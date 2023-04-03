from __future__ import annotations

import os
from dataclasses import dataclass
from subprocess import Popen
from typing import Tuple

import cv2
import ffmpeg
import numpy as np
from sanic.log import logger

from process import IteratorContext

from ...impl.image_utils import normalize, to_uint8
from ...node_base import IteratorNodeBase, NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import (
    IteratorInput,
    VideoFileInput,
)
from ...properties.outputs import DirectoryOutput, ImageOutput, NumberOutput, TextOutput
from ...utils.utils import get_h_w_c, split_file_path
from . import category as ImageCategory

VIDEO_ITERATOR_INPUT_NODE_ID = "machines:image:simple_video_frame_iterator_load"
# VIDEO_ITERATOR_OUTPUT_NODE_ID = "machines:image:simple_video_frame_iterator_save"

ffmpeg_path = os.environ.get("STATIC_FFMPEG_PATH", "ffmpeg")
ffprobe_path = os.environ.get("STATIC_FFPROBE_PATH", "ffprobe")

codec_map = {
    "mp4": "libx264",
    "avi": "libx264",
    "mkv": "libx264",
    "webm": "libvpx-vp9",
    "gif": "gif",
}


@dataclass
class Writer:
    out: Popen | None = None
    copy_audio: bool = False
    video_save_path: str | None = None


@NodeFactory.register(VIDEO_ITERATOR_INPUT_NODE_ID)
class VideoFrameIteratorFrameLoaderNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = ""
        self.inputs = [IteratorInput().make_optional()]
        self.outputs = [
            ImageOutput("Data ->", channels=3),
            NumberOutput("Index"),
            DirectoryOutput("Data Directory"),
            TextOutput("Plot out"),
        ]

        self.category = ImageCategory
        self.name = "Timeseries"
        self.icon = "MdSubdirectoryArrowRight"
        self.sub = "Iteration"

        self.type = "iteratorHelper"

        self.side_effects = True

    def run(
        self, img: np.ndarray, idx: int, video_dir: str, video_name: str
    ) -> Tuple[np.ndarray, int, str, str]:
        return normalize(img), idx, video_dir, video_name



@NodeFactory.register("machines:image:video_frame_iterator")
class SimpleVideoFrameIteratorNode(IteratorNodeBase):
    def __init__(self):
        super().__init__()
        self.description = (
            "runs a live graph."
        )
        self.inputs = [
            VideoFileInput(primary_input=True),
        ]
        self.outputs = []
        self.default_nodes = [
            # TODO: Figure out a better way to do this
            {
                "schemaId": VIDEO_ITERATOR_INPUT_NODE_ID,
            },
            # {
            #     "schemaId": VIDEO_ITERATOR_OUTPUT_NODE_ID,
            # },
        ]

        self.category = ImageCategory
        self.name = "Live Data Viewer"
        # self.icon = "MdVideoCameraBack"

    # pylint: disable=invalid-overridden-method
    async def run(self, path: str, context: IteratorContext) -> None:
        logger.debug(f"{ffmpeg_path=}, {ffprobe_path=}")
        logger.debug(f"Iterating over frames in video file: {path}")

        input_node_id = context.get_helper(VIDEO_ITERATOR_INPUT_NODE_ID).id
        # output_node_id = context.get_helper(VIDEO_ITERATOR_OUTPUT_NODE_ID).id

        video_dir, video_name, _ = split_file_path(path)

        ffmpeg_reader = (
            ffmpeg.input(path)
            .output("pipe:", format="rawvideo", pix_fmt="rgb24")
            .run_async(pipe_stdout=True, cmd=ffmpeg_path)
        )

        writer = Writer()

        probe = ffmpeg.probe(path, cmd=ffprobe_path)
        video_format = probe.get("format", None)
        if video_format is None:
            raise RuntimeError("Failed to get video format. Please report.")
        video_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )

        if video_stream is None:
            raise RuntimeError("No video stream found in file")

        width = video_stream.get("width", None)
        if width is None:
            raise RuntimeError("No width found in video stream")
        width = int(width)
        height = video_stream.get("height", None)
        if height is None:
            raise RuntimeError("No height found in video stream")
        height = int(height)
        fps = video_stream.get("r_frame_rate", None)
        if fps is None:
            raise RuntimeError("No fps found in video stream")
        fps = int(fps.split("/")[0]) / int(fps.split("/")[1])
        frame_count = video_stream.get("nb_frames", None)
        if frame_count is None:
            duration = video_stream.get("duration", None)
            if duration is None:
                duration = video_format.get("duration", None)
            if duration is not None:
                frame_count = float(duration) * fps
            else:
                raise RuntimeError(
                    "No frame count or duration found in video stream. Unable to determine video length. Please report."
                )
        frame_count = int(frame_count)

        # context.inputs.set_append_values(output_node_id, [writer, fps])

        def before(index: int):
            in_bytes = ffmpeg_reader.stdout.read(width * height * 3)
            if not in_bytes:
                print("Can't receive frame (stream end?). Exiting ...")
                return False
            in_frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])
            in_frame = cv2.cvtColor(in_frame, cv2.COLOR_RGB2BGR)

            # todo: reuse this for reactive machines!
            context.inputs.set_values(
                input_node_id, [in_frame, index, video_dir, video_name]
            )

        await context.run_while(frame_count, before, fail_fast=True)

        ffmpeg_reader.stdout.close()
        ffmpeg_reader.wait()
        if writer.out is not None:
            if writer.out.stdin is not None:
                writer.out.stdin.close()
            writer.out.wait()

        if writer.copy_audio and writer.video_save_path is not None:
            out_path = writer.video_save_path
            base, ext = os.path.splitext(out_path)
            if "gif" not in ext.lower():
                full_out_path = f"{base}_audio{ext}"
                audio_stream = ffmpeg.input(path).audio
                video_stream = ffmpeg.input(out_path)
                output_video = ffmpeg.output(
                    audio_stream,
                    video_stream,
                    full_out_path,
                    vcodec="copy",
                ).overwrite_output()
                ffmpeg.run(output_video)
                # delete original, rename new
                os.remove(out_path)
                os.rename(full_out_path, out_path)
