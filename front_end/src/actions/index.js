// DUMMY VENUE DATA
import venues from './venues'
import menus from './menus'
const ROOT_URL = "https://fncflnxl03.execute-api.eu-west-2.amazonaws.com/testing"
const proxyurl = "https://cors-anywhere.herokuapp.com/"

export const FETCH_VENUES = 'FETCH_VENUES';
export function setVenues(search_obj) {
    const ROOT_URL = "https://fncflnxl03.execute-api.eu-west-2.amazonaws.com/testing/"
    const proxyurl = "https://cors-anywhere.herokuapp.com/"
    let query = `?query=${search_obj["query"]}&pricemin=${search_obj["pricemin"]}&pricemax=${search_obj["pricemax"]}&latitude=${search_obj["latitude"]}&longitude=${search_obj["longitude"]}&radius=${search_obj["radius"]}&restaurants=${search_obj["restaurants"]}&bars=${search_obj["bars"]}&cafes=${search_obj["cafes"]}`
    const promise = fetch(`${proxyurl}${ROOT_URL}/fetch-venues${query}`, {headers: {'Access-Control-Allow-Origin': '*'}})
    .then(response => response.json())
    .then((data => {
      return data
    }))

    return {
      type: FETCH_VENUES,
      payload: promise
    }
}

export const EMPTY_VENUES = "EMPTY_VENUES";
export function emptyVenues() {
  return {
    type: EMPTY_VENUES
  }
}

export const TOGGLE_FILTER = "TOGGLE_FILTER";
export function toggleFilter(filter) {
  return {
    type: TOGGLE_FILTER,
    payload: filter
  }
}

export const UPDATE_SEARCH = "UPDATE_SEARCH";
export function updateSearch(newSearch) {
  return {
    type: UPDATE_SEARCH,
    payload: newSearch
  }
}

export const FETCH_VENUE = 'FETCH_VENUE';
export function fetchVenue(venueid, typeid) {
  const promise = fetch(`${proxyurl}${ROOT_URL}/get-venue?venueid=${venueid}&typeid=${typeid}`, {headers: {'Access-Control-Allow-Origin': '*'}})
    .then(response => response.json())
    .then((data => {
      return [JSON.parse(data.body)]
    }))

    return {
      type: FETCH_VENUE,
      payload: promise
    }
}


export const FETCH_MENU = 'FETCH_MENU';
export function fetchMenu(venueid, typeid) {
  const promise = fetch(`${proxyurl}${ROOT_URL}/get-menu?venueid=${venueid}&typeid=${typeid}`, {headers: {'Access-Control-Allow-Origin': '*'}})
    .then(response => response.json())
    .then((data => {
      return JSON.parse(data.body)
    })).catch((error) => {
      console.log(error.message);
    })

    return {
      type: FETCH_MENU,
      payload: promise
    }
}


export const EMPTY_MENU = 'EMPTY_MENU';
export function emptyMenu(venueid, typeid) {
  return {
    type: EMPTY_MENU,
    payload: {}
  }
}

export const TOGGLE_MAP = 'TOGGLE_MAP';
export function toggleMap() {
  return {
    type: TOGGLE_MAP
  }
}

export const ADD_TO_BASKET = 'ADD_TO_BASKET';
export function addToBasket(item) {
  return {
    type: ADD_TO_BASKET,
    payload: item
  }
}

export const REMOVE_FROM_BASKET = 'REMOVE_FROM_BASKET';
export function removeFromBasket(item) {
  return {
    type: REMOVE_FROM_BASKET,
    payload: item
  }
}

export const EMPTY_BASKET = 'EMPTY_BASKET';
export function emptyBasket() {
  return {
    type: EMPTY_BASKET
  }
}

export const POST_POSTCODE = "POST_POSTCODE";
export function postPostcode(postcode) {
  return {
    type: POST_POSTCODE,
    payload: postcode
  }
}

export const SET_CENTER = "SET_CENTER";
export function setCenter(postcode) {
    const promise = fetch(`https://api.postcodes.io/postcodes/${postcode.replace(/ /g, '')}`)
      .then(res => res.json())          // convert to plain text
      .then((data) => {
        return data
  })
  return {
    type: SET_CENTER,
    payload: promise
  }
}

export const SET_USER_LOC = "SET_USER_LOC";
export function setUserLoc(loc) {
  return {
    type: SET_USER_LOC,
    payload: loc
  }
}

export const SORT_BY_PRICE_LOW = "SORT_BY_PRICE_LOW";
export function sortByPriceLow() {
  return {
    type: SORT_BY_PRICE_LOW
  }
}

export const SORT_BY_PRICE_HIGH = "SORT_BY_PRICE_HIGH";
export function sortByPriceHigh() {
  return {
    type: SORT_BY_PRICE_HIGH
  }
}

export const SORT_BY_DISTANCE = "SORT_BY_DISTANCE";
export function sortByDistance(user_loc) {
  return {
    type: SORT_BY_DISTANCE,
    payload: user_loc
  }
}


