import { createSlice } from '@reduxjs/toolkit'

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

export const useridSlice = createSlice({
    name: 'userid',
    initialState: getCookie("userid"),
    reducers: {}
});

export default useridSlice.reducer;
