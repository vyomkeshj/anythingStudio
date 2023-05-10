from typing import Any, List, Literal, Optional, Tuple, TypedDict, Union

from base_types import NodeId

from .nmgraph import NMGraph, Edge, EdgeSource, EdgeTarget, FunctionNode, IteratorNode, OutputChannel
from .input import EdgeInput, Input, InputMap, ValueInput


class JsonEdgeInput(TypedDict):
    type: Literal["edge"]
    id: NodeId
    index: int


class JsonValueInput(TypedDict):
    type: Literal["value"]
    value: Any


JsonInput = Union[JsonEdgeInput, JsonValueInput]


class JsonNode(TypedDict):
    id: NodeId
    schemaId: str
    inputs: List[JsonInput]
    output_channels: List[OutputChannel]
    parent: Optional[NodeId]
    nodeType: str


class IndexEdge:
    def __init__(
        self, from_id: NodeId, from_index: int, to_id: NodeId, to_index: int
    ) -> None:
        self.from_id = from_id
        self.from_index = from_index
        self.to_id = to_id
        self.to_index = to_index


def parse_json(json: List[JsonNode]) -> Tuple[NMGraph, InputMap]:
    nm_graph = NMGraph()
    input_map = InputMap()

    index_edges: List[IndexEdge] = []

    for json_node in json:
        if json_node["nodeType"] == "iterator":
            #
            node = IteratorNode(json_node["id"], json_node["schemaId"], json_node["output_channels"])
        else:
            node = FunctionNode(json_node["id"], json_node["schemaId"], json_node["output_channels"])
            node.parent = json_node["parent"]
            node.is_helper = json_node["nodeType"] == "iteratorHelper"
        nm_graph.add_node(node)

        inputs: List[Input] = []
        for index, i in enumerate(json_node["inputs"]):
            if i["type"] == "edge":
                inputs.append(EdgeInput(i["id"], i["index"]))
                index_edges.append(IndexEdge(i["id"], i["index"], node.id, index))
            else:
                inputs.append(ValueInput(i["value"]))
        input_map.set(node.id, inputs)

    for index_edge in index_edges:
        source_node = nm_graph.nodes[index_edge.from_id].get_node()
        target_node = nm_graph.nodes[index_edge.to_id].get_node()

        #todo: create subscription hererere!
        nm_graph.add_edge(
            Edge(
                EdgeSource(
                    index_edge.from_id,
                    source_node.outputs[index_edge.from_index].id,
                ),
                EdgeTarget(
                    index_edge.to_id,
                    target_node.inputs[index_edge.to_index].id,
                ),
            )
        )

    return nm_graph, input_map
