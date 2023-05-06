import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import {ExpressionJson} from "../../../common/types/json";
import {OutputChannel, OutputId, OutputKind} from "../../../common/common-types";
import {Type} from "@chainner/navi";
import produce from "immer";
import {UiBuilderComponentsState} from "./uiBuilderComponentsSlice";

export interface node {
    id: string;
    type: ExpressionJson;
    neverReason?: string | null;
    label: string;
    kind: OutputKind;
    ui_message_registry: OutputChannel[];
    outputId: OutputId;
    useOutputData: Function;
    schemaId: string;
    definitionType: Type;
    hasHandle: boolean;
    animated: undefined | boolean;
    jsx: JSX.Element;
}
interface NodesState {
    outputNodes: node[];
}

const initialState: NodesState = {
    outputNodes: [],
};

export const nodesSlice = createSlice({
    name: 'nodes',
    initialState,
    reducers: {
        addNode: (state, node: node) => {
            console.log(node)
            return produce(state, (draftState: NodesState) => {
                draftState.outputNodes.push(node);
            })
        },
        removeNode: (state, id: string) => {
            state.outputNodes = state.outputNodes.filter((node) => node.id !== id)
        },
    },
});

export const { addNode, removeNode } = nodesSlice.actions;
export default nodesSlice.reducer;
