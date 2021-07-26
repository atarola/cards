import { createSlice } from '@reduxjs/toolkit'
import get from 'lodash.get';

const initialState = {
    state: "",
    players: {},
    dealerScore: 0,
};

export const statusSlice = createSlice({
    name: 'counter',
    initialState,
    reducers: {
        status: (state, action) => {
            state.state = get(action.payload, "state", "");
            state.players = get(action.payload, "tableu", {});
            state.dealerScore = get(action.payload, "tableu.dealer.value", 0);
        },
    }
});

export const { status } = statusSlice.actions;
export default statusSlice.reducer;
