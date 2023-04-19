import asyncio
from abc import ABCMeta, abstractmethod
from typing import Any, List, Literal, Union, NewType

from base_types import InputId, OutputId, NodeId

from .category import Category
from .group import Group, GroupId, NestedGroup, NestedIdGroup
from .io.inputs.base_input import BaseInput
from .io.outputs.base_output import BaseOutput
# from reactivex.subject import Subject
from src.events import UIEventChannel

NodeType = Literal["regularNode", "iterator", "iteratorHelper"]


class NodeBase(metaclass=ABCMeta):
    """Base class for a node"""

    def __init__(self):
        self.__inputs: List[BaseInput] = []
        self.__outputs: List[BaseOutput] = []
        self.__group_layout: List[Union[InputId, NestedIdGroup]] = []
        self.description: str = ""

        self.category: Category = Category(
            "Unknown", "Unknown category", "BsQuestionDiamond", "#718096"
        )
        self.name: str = ""
        self.icon: str = ""
        self.sub: str = "Miscellaneous"
        self.type: NodeType = "regularNode"

        self.side_effects: bool = False
        self.deprecated: bool = False

        self.node_id: NodeId = None

        self.event_loop: asyncio.AbstractEventLoop = None   # type: ignore

    def set_node_id(self, node_id: NodeId):
        self.node_id = node_id

    def set_output_id_for_channel(self, channel_name: str, channel_id: str):
        # fixme: assumes channel names are never same across outputs
        for output in self.outputs:
            output.set_channel_id_by_name(channel_name, channel_id)

    def set_event_loop(self, event_loop):
        self.event_loop = event_loop

    @property
    def inputs(self) -> List[BaseInput]:
        return self.__inputs

    @inputs.setter
    def inputs(self, value: List[Union[BaseInput, NestedGroup]]):
        inputs: List[BaseInput] = []
        groups = []

        def add_inputs(
            current: List[Union[BaseInput, NestedGroup]]
        ) -> List[Union[InputId, NestedIdGroup]]:
            layout: List[Union[InputId, NestedIdGroup]] = []

            for x in current:
                if isinstance(x, Group):
                    if x.info.id == -1:
                        x.info.id = GroupId(len(groups))
                    g: NestedIdGroup = Group(x.info, [])
                    groups.append(g)
                    layout.append(g)
                    g.items.extend(add_inputs(x.items))  # type: ignore
                else:
                    if x.id == -1:
                        x.id = InputId(len(inputs))
                    layout.append(x.id)
                    inputs.append(x)

            return layout

        self.__inputs = inputs
        self.__group_layout = add_inputs(value)

    @property
    def outputs(self) -> List[BaseOutput]:
        return self.__outputs

    @outputs.setter
    def outputs(self, value: List[BaseOutput]):
        for i, output_value in enumerate(value):
            if output_value.id == -1:
                output_value.id = OutputId(i)
        self.__outputs = value

    @property
    def group_layout(self) -> List[Union[InputId, NestedIdGroup]]:
        return self.__group_layout

    def get_outputs(self) -> List[BaseOutput]:
        return self.__outputs

    @abstractmethod
    def run(self) -> Any:
        """Abstract method to run a node's logic"""
        return


# pylint: disable=abstract-method
class IteratorNodeBase(NodeBase):
    """Base class for an iterator node"""

    def __init__(self):
        super().__init__()
        self.icon = "MdLoop"
        self.sub = "Iteration"
        self.type = "iterator"
        self.default_nodes = []

        self.side_effects = True

    def get_default_nodes(self):
        return self.default_nodes