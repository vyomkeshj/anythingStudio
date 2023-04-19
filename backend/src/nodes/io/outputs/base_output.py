from __future__ import annotations

from typing import Literal, Union, List

from base_types import OutputId
import json

from src.events import UIEventChannel, ToUIOutputMessage, UIEvtChannelSchema
from .. import expression

OutputKind = Literal["dataframe", "chat", "image", "large-image", "tagged", "generic"]


class BaseOutput:
    def __init__(
            self,
            output_type: expression.ExpressionJson,
            label: str,
            kind: OutputKind = "generic",
            has_handle: bool = True,
            channels=None,
    ):
        if channels is None:
            channels = []

        self.output_type: expression.ExpressionJson = output_type
        self.label: str = label
        self.id: OutputId = OutputId(-1)
        self.never_reason: Union[str, None] = None

        # if the component is a live component
        self.ui_message_registry: List[UIEvtChannelSchema] = channels
        self.uplink_channel: UIEventChannel = None  # type ignore
        self.kind: OutputKind = kind
        self.has_handle: bool = has_handle

    def toDict(self):
        return {
            "id": self.id,
            "type": self.output_type,
            "label": self.label,
            "neverReason": self.never_reason,
            "kind": self.kind,
            "hasHandle": self.has_handle,
            "ui_message_registry": self.ui_message_registry,
        }

    def get_channel_id_by_name(self, channel_name: str):
        for channel in self.ui_message_registry:
            if channel['channel_name'] == channel_name:
                return channel['channel_id']
        return None

    def set_channel_id_by_name(self, channel_name: str, channel_id: str):
        for channel in self.ui_message_registry:
            if channel['channel_name'] == channel_name:
                channel['channel_id'] = channel_id
                return
        return None

    def provide_channel_to_output(self, channel: UIEventChannel):
        """When the nodes are received from the ui, the backend provides the nodes channels to comm with the ui"""
        self.uplink_channel = channel

    async def send_ui_event(self, event: ToUIOutputMessage):
        await self.uplink_channel.put(event)

    async def receive_ui_event(self, channel_name: str):
        # fixme: incorrect
        return await self.uplink_channel.get()

    def with_id(self, output_id: Union[OutputId, int]):
        self.id = OutputId(output_id)
        return self

    def with_never_reason(self, reason: str):
        self.never_reason = reason
        return self

    def __repr__(self):
        return str(self.toDict())

    def __iter__(self):
        yield from self.toDict().items()

    def get_broadcast_data(self, _value):
        return None

    def get_broadcast_type(self, _value) -> expression.ExpressionJson | None:
        return None

    def validate(self, value) -> None:
        assert value is not None
