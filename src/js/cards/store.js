import { configureStore } from '@reduxjs/toolkit'

import statusReducer from './slices/status';
import useridReducer from './slices/userid';

export const store = configureStore({
    reducer: {
        status: statusReducer,
        userid: useridReducer,
    },
});
