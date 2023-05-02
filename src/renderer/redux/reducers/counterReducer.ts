import { AppState } from '../types';

interface IncrementAction {
    type: 'INCREMENT';
}

interface DecrementAction {
    type: 'DECREMENT';
}

type Action = IncrementAction | DecrementAction;

const initialState: AppState = {
    counter: 0
};

function counterReducer(state = initialState, action: Action): AppState {
    switch (action.type) {
        case 'INCREMENT':
            return { ...state, counter: state.counter + 1 };
        case 'DECREMENT':
            return { ...state, counter: state.counter - 1 };
        default:
            return state;
    }
}

export default counterReducer;
