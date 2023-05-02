import { init } from '@rematch/core';
import { combineReducers } from 'redux';
import undoable from 'redux-undo';
import { persistReducer, persistStore } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import models from './models';
import filterUndoableActions from '../utils/undo';

import { ComponentsStateWithUndo } from './models/components';
import { AppState } from './models/app';

export type RootState = {
  app: AppState;
  components: ComponentsStateWithUndo;
};

const version = parseInt(process.env.VERSION || '1', 10);

const persistConfig = {
  key: `openchakra_v${version}`,
  storage,
  whitelist: ['present'],
  version,
  throttle: 500,
};

const persistPlugin = {
  onStoreCreated(store: any) {
    persistStore(store);
  },
};

export const storeConfig = {
  models,
  redux: {
    combineReducers: (reducers: any) => {
      return combineReducers({
        ...reducers,
        components: persistReducer(
            persistConfig,
            undoable(reducers.components, {
              limit: 10,
              filter: filterUndoableActions,
            }),
        ),
      });
    },
  },
  plugins: [persistPlugin],
};

export const makeStore = () => init(storeConfig);


export const wrapper = createWrapper<RootState>(makeStore)
