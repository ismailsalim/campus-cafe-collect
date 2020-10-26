import { ADD_TO_BASKET, REMOVE_FROM_BASKET, EMPTY_BASKET } from '../actions';
import { add_item } from '../helpers/basket'
import { remove_item } from '../helpers/basket'


let basket_template = {
  total: 0.00,
  items: {},
  venue: -1,
  venueid: -1,
  typeid: -1,
  venue_stripe_acct: ""
}

const basketReducer = (state, action) => {
  if (state === undefined) {
    // Reducer initialisation
    return basket_template;
  }

  // Handle Venues Actions
  switch (action.type) {
    case ADD_TO_BASKET:
      return add_item(state, action.payload);
    case REMOVE_FROM_BASKET:
      return remove_item(state, action.payload);
    case EMPTY_BASKET:
      return basket_template;
    default:
      return state;
  }

};
export default basketReducer;








