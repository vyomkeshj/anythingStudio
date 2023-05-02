import { combineReducers } from 'redux';
import counterReducer from './counterReducer';
import { AppState } from '../types';

const rootReducer = combineReducers({
    counter: counterReducer
});

export type RootState = ReturnType<typeof rootReducer>;

export default rootReducer;
