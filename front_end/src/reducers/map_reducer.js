import { TOGGLE_MAP } from '../actions';

const mapReducer = (state, action) => {
  if (state === undefined) {
    // Reducer initialisation
    return [];
  }

  // Handle Venues Actions
  switch (action.type) {
    case TOGGLE_MAP:
      return !state;
    default:
      return state;
  }

};
export default mapReducer;
