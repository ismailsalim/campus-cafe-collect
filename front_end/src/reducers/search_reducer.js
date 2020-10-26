import { TOGGLE_FILTER, UPDATE_SEARCH } from '../actions';

const base_search = {
  "query": "",
  "pricemin": 1,
  "pricemax": 3,
  "latitude": 51.4988,
  "longitude": -0.1749,
  "radius": 5,
  "restaurants": true,
  "bars": true,
  "cafes": true
}

const searchReducer = (state, action) => {

  if (state === undefined) {
    // Reducer initialisation
    return base_search;
  }

  // Handle Venues Actions
  switch (action.type) {
    case TOGGLE_FILTER:
      let newSearch = {...state}
      newSearch[action.payload] = !state[action.payload]
      return newSearch
    case UPDATE_SEARCH:
      return action.payload
    default:
      return state;
  }

};
export default searchReducer;
