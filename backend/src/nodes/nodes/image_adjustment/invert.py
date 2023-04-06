from __future__ import annotations

import numpy as np

from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...io.inputs import ImageInput
from ...io.outputs import ImageOutput
from ...utils.utils import get_h_w_c
from . import category as ImageAdjustmentCategory


@NodeFactory.register("machines:image:invert")
class InvertNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Inverts all colors in an image."
        self.inputs = [ImageInput()]
        self.outputs = [ImageOutput(image_type="Input0")]
        self.category = ImageAdjustmentCategory
        self.name = "Detect Outliers"
        self.icon = "MdInvertColors"
        self.sub = "Data ops"

    def run(self, img: np.ndarray) -> np.ndarray:
        c = get_h_w_c(img)[2]

        # invert the first 3 channels
        if c <= 3:
            return 1 - img

        img = img.copy()
        img[:, :, :3] = 1 - img[:, :, :3]
        return img
