import { combineReducers } from '@reduxjs/toolkit';
import counterReducer from './slices/counterSlice';
import settingsReducer from './slices/settingsSlice';

const rootReducer = combineReducers({
    counter: counterReducer,
    settings: settingsReducer,
});

export default rootReducer;
