import { SET_CENTER } from '../actions';

const centerReducer = (state, action) => {
  if (state === undefined) {
    // Reducer initialisation
    return [];
  }

  // Handle Venues Actions
  switch (action.type) {
    case SET_CENTER:
      return (action.payload.status == 200) ? [action.payload.result.longitude, action.payload.result.latitude] : [0,0];
    default:
      return state;
  }

};
export default centerReducer;
