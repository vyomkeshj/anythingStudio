import { combineReducers } from '@reduxjs/toolkit';
import counterReducer from './slices/counterSlice';
import nodesSlice from './slices/nodesSlice';
import settingsReducer from './slices/settingsSlice';
import uiBuilderReducer from './slices/uiBuilderSlice';
import uiBuilderComponentsReducer from './slices/uiBuilderComponentsSlice';

const rootReducer = combineReducers({
    counter: counterReducer,
    nodes: nodesSlice,
    settings: settingsReducer,
    builder: uiBuilderReducer,
    builderComponents: uiBuilderComponentsReducer,
});

export default rootReducer;
