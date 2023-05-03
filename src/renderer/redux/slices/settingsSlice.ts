import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface SettingsState {
    tab: number;
}

const initialState: SettingsState = {
    tab: 0,
};

export const settingsSlice = createSlice({
    name: 'settings',
    initialState,
    reducers: {
        switchToDesigner: (state) => {
            state.tab = 1;
        },
        switchToEngine: (state) => {
            state.tab = 0;
        },
    },
});

export const { switchToDesigner, switchToEngine } = settingsSlice.actions;
export default settingsSlice.reducer;
