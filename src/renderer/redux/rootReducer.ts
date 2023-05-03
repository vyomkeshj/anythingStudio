import { combineReducers } from '@reduxjs/toolkit';
import counterReducer from './slices/counterSlice';
import settingsReducer from './slices/settingsSlice';
import uiBuilderReducer from './slices/uiBuilderSlice';
import uiBuilderComponentsReducer from './slices/uiBuilderComponentsSlice';

const rootReducer = combineReducers({
    counter: counterReducer,
    settings: settingsReducer,
    builder: uiBuilderReducer,
    builderComponents: uiBuilderComponentsReducer,
});

export default rootReducer;
