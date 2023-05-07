import { createSlice } from '@reduxjs/toolkit';
import {OutputChannel, OutputId, OutputKind} from "../../../common/common-types";
import produce from "immer";

export interface MachinesNodeUI {
    id: string;
    label: string;
    kind: OutputKind;
    ui_message_registry: OutputChannel[];
    outputId: OutputId;
    schemaId: string;
}
export interface NodesState {
    outputNodes: MachinesNodeUI[];
}

const initialState: NodesState = {
    outputNodes: [],
};

export const machinesNodesSlice = createSlice({
    name: 'nodes',
    initialState,
    reducers: {
        addNode: (state, node: MachinesNodeUI) => {
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

export const { addNode, removeNode } = machinesNodesSlice.actions;
export default machinesNodesSlice.reducer;
