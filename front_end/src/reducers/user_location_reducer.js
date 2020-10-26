import { SET_USER_LOC } from '../actions';

const userLocationReducer = (state, action) => {
  if (state === undefined) {
    // Reducer initialisation
    return [];
  }

  // Handle Venues Actions
  switch (action.type) {
    case SET_USER_LOC:
      return action.payload;
    default:
      return state;
  }

};
export default userLocationReducer;
