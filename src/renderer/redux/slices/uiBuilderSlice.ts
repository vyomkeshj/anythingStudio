import { createSlice, PayloadAction } from '@reduxjs/toolkit';

type Overlay = undefined | { rect: DOMRect; id: string; type: ComponentType }

export type UiBuilderState = {
    showLayout: boolean
    showCode: boolean
    inputTextFocused: boolean
    overlay: undefined | Overlay
    // todo: nodes list
}

const initialState: UiBuilderState = {
    showLayout: true,
    showCode: false,
    inputTextFocused: false,
    overlay: undefined,
};

export const uiBuilderSlice = createSlice({
    name: 'builder',
    initialState,
    reducers: {
        toggleBuilderMode(state): UiBuilderState {
            return {
                ...state,
                showLayout: !state.showLayout,
            }
        },
        toggleCodePanel(state: UiBuilderState): UiBuilderState {
            return {
                ...state,
                showCode: !state.showCode,
            }
        },
        toggleInputText(state: UiBuilderState): UiBuilderState {
            return {
                ...state,
                inputTextFocused: !state.inputTextFocused,
            }
        },
        setOverlay(state: UiBuilderState, { payload }: { payload: { overlay: Overlay | undefined }}): UiBuilderState {
            return {
                ...state,
                overlay: payload.overlay,
            }
        },
        'builderComponents/deleteComponent': (state: UiBuilderState): UiBuilderState => {
            return {
                ...state,
                overlay: undefined,
            }
        },
        '@@redux-undo/UNDO': (state: UiBuilderState): UiBuilderState => {
            return {
                ...state,
                overlay: undefined,
            }
        },
    },
});

export const {
    toggleBuilderMode,
    toggleCodePanel,
    toggleInputText,
    setOverlay,
} = uiBuilderSlice.actions;
export default uiBuilderSlice.reducer;
