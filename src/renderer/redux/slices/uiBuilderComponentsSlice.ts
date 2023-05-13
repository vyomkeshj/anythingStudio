import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import {ComponentType} from "react";
import produce from "immer";
import {DEFAULT_PROPS} from "../../utils/defaultProps";
import omit from "lodash/omit";
import { deleteComponent as deleteComponentFunc, duplicateComponent } from "../../utils/recursive";
import {generateId} from "../../utils/generateId";
import { IComponent, IComponents } from "../../../react-app-env";

export type UiBuilderComponentsState = {
    present: any;
    components: IComponents
    selectedId: IComponent['id']
    hoveredId?: IComponent['id']
}

export type UiBuilderComponentsStateWithUndo = {
    past: UiBuilderComponentsState[]
    present: UiBuilderComponentsState
    future: UiBuilderComponentsState[]
}

const DEFAULT_ID = 'root'

export const INITIAL_COMPONENTS: IComponents = {
    root: {
        id: DEFAULT_ID,
        parent: DEFAULT_ID,
// @ts-ignore
        type: 'Box' as ComponentType,
        children: [],
        props: {},
    },
}

const initialState: UiBuilderComponentsState = {
    components: INITIAL_COMPONENTS,
    selectedId: DEFAULT_ID,
    present: {components: {}},
    hoveredId: undefined
};

export const uiBuilderComponentsSlice = createSlice({
    name: 'builderComponents',
    initialState,
    reducers: {
        reset(state: UiBuilderComponentsState, { payload }) {
            state.components = payload.components || INITIAL_COMPONENTS
            state.selectedId = DEFAULT_ID
        },
        resetProps(state: UiBuilderComponentsState, { payload }: {payload: {componentId: string}}): UiBuilderComponentsState {
            return produce(state, (draftState: UiBuilderComponentsState) => {
                draftState.components[payload.componentId].props = DEFAULT_PROPS || {}
            })
        },
        updateProps(
            state: UiBuilderComponentsState,
            { payload }: { payload: { id: string; name: string; value: string }},
        ) {
            return produce(state, (draftState: UiBuilderComponentsState) => {
                draftState.components[payload.id].props[payload.name] = payload.value
            })
        },
        deleteProps(state: UiBuilderComponentsState, { payload }: { payload: { id: string; name: string }}) {
            return {
                ...state,
                components: {
                    ...state.components,
                    [payload.id]: {
                        ...state.components[payload.id],
                        props: omit(state.components[payload.id].props, payload.name),
                    },
                },
            }
        },
        deleteComponent(state: UiBuilderComponentsState, { payload }: { payload: { componentId: string }}) {
            if (payload.componentId === 'root') {
                return state
            }

            return produce(state, (draftState: UiBuilderComponentsState) => {
                let component = draftState.components[payload.componentId]

                // Remove self
                if (component && component.parent) {
                    const children = draftState.components[
                        component.parent
                        ].children.filter((id: string) => id !== payload.componentId)

                    draftState.components[component.parent].children = children
                }

                draftState.selectedId = DEFAULT_ID
                draftState.components = deleteComponentFunc(
                    component,
                    draftState.components,
                )
            })
        },
        moveComponent(
            state: UiBuilderComponentsState,
            {payload}: {payload: { parentId: string; componentId: string }},
        ): UiBuilderComponentsState {
            if (
                state.components[payload.componentId].parent === payload.parentId ||
                payload.parentId === payload.componentId
            ) {
                return state
            }

            return produce(state, (draftState: UiBuilderComponentsState) => {
                const previousParentId =
                    draftState.components[payload.componentId].parent

                const children = draftState.components[
                    previousParentId
                    ].children.filter(id => id !== payload.componentId)

                // Remove id from previous parent
                draftState.components[previousParentId].children = children

                // Update parent id
                draftState.components[payload.componentId].parent = payload.parentId

                // Add new child
                draftState.components[payload.parentId].children.push(
                    payload.componentId,
                )
            })
        },
        moveSelectedComponentChildren(
            state: UiBuilderComponentsState,
            {payload}: { payload: { fromIndex: number; toIndex: number }},
        ): UiBuilderComponentsState {
            return produce(state, (draftState: UiBuilderComponentsState) => {
                const selectedComponent = draftState.components[draftState.selectedId]

                selectedComponent.children.splice(
                    payload.toIndex,
                    0,
                    selectedComponent.children.splice(payload.fromIndex, 1)[0],
                )
            })
        },
        addComponent(
            state: UiBuilderComponentsState,
            {payload}: {payload: {
                parentName: string
                type: ComponentType | string
                rootParentType?: ComponentType | string
                testId?: string
            }},
        ): UiBuilderComponentsState {
            return produce(state, (draftState: UiBuilderComponentsState) => {
                const id = payload.testId || generateId()
                // @ts-ignore
                const { form, ...defaultProps } = DEFAULT_PROPS[payload.type] || {}
                draftState.selectedId = id
                draftState.components[payload.parentName].children.push(id)
                draftState.components[id] = {
                    id,
                    props: defaultProps || {},
                    children: [],
                    // @ts-ignore
                    type: payload.type,
                    parent: payload.parentName,
                    // @ts-ignore
                    rootParentType: payload.rootParentType || payload.type,
                }
            })
        },
        addMetaComponent(
            state: UiBuilderComponentsState,
            {payload}: {payload: { components: IComponents; root: string; parent: string }},
        ): UiBuilderComponentsState {
            return produce(state, (draftState: UiBuilderComponentsState) => {
                draftState.selectedId = payload.root
                draftState.components[payload.parent].children.push(payload.root)

                draftState.components = {
                    ...draftState.components,
                    ...payload.components,
                }
            })
        },
        select(
            state: UiBuilderComponentsState,
            {payload}: {payload: { selectedId: IComponent['id']}},
        ) {
            state.selectedId = payload.selectedId
        },
        unselect(state: UiBuilderComponentsState) {
            state.selectedId = DEFAULT_ID
        },
        selectParent(state: UiBuilderComponentsState) {
            const selectedComponent = state.components[state.selectedId]
            state.selectedId = state.components[selectedComponent.parent].id
        },
        duplicate(state: UiBuilderComponentsState): UiBuilderComponentsState {
            return produce(state, (draftState: UiBuilderComponentsState) => {
                const selectedComponent = draftState.components[draftState.selectedId]

                if (selectedComponent.id !== DEFAULT_ID) {
                    const parentElement = draftState.components[selectedComponent.parent]

                    const { newId, clonedComponents } = duplicateComponent(
                        selectedComponent,
                        draftState.components,
                    )

                    draftState.components = {
                        ...draftState.components,
                        ...clonedComponents,
                    }
                    draftState.components[parentElement.id].children.push(newId)
                }
            })
        },
        setComponentName(
            state: UiBuilderComponentsState,
            {payload}: { payload: { componentId: string; name: string }},
        ): UiBuilderComponentsState {
            return produce(state, draftState => {
                const component = draftState.components[payload.componentId]

                component.componentName = payload.name
            })
        },
        hover(
            state: UiBuilderComponentsState,
            {payload}: { payload: { componentId: IComponent['id'] }},
        ): UiBuilderComponentsState {
            return {
                ...state,
                hoveredId: payload.componentId,
            }
        },
        unhover(state: UiBuilderComponentsState) {
            state.hoveredId = undefined
        },
    },
});

export const { reset,
    resetProps,
    updateProps,
    deleteProps,
    deleteComponent,
    moveComponent,
    moveSelectedComponentChildren,
    addComponent,
    addMetaComponent,
    select,
    unselect,
    selectParent,
    duplicate,
    setComponentName,
    hover,
    unhover } = uiBuilderComponentsSlice.actions;
export default uiBuilderComponentsSlice.reducer;
