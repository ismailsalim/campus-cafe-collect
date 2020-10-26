import React, { Component, lazy, Suspense } from 'react'
import ReactDOM from 'react-dom';
import '../assets/stylesheets/application.scss';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

import { Provider } from 'react-redux';
import { createStore, combineReducers, applyMiddleware, compose } from 'redux';
import { logger } from 'redux-logger';
import reduxPromise from 'redux-promise';

import venuesReducer from './reducers/venues_reducer'
import menuReducer from './reducers/menu_reducer'
import mapReducer from './reducers/map_reducer'
import basketReducer from './reducers/basket_reducer'
import postcodeReducer from './reducers/postcode_reducer'
import centerReducer from './reducers/center_reducer'
import userLocationReducer from './reducers/user_location_reducer'
import searchReducer from './reducers/search_reducer'


import API from '@aws-amplify/api'
import PubSub from '@aws-amplify/pubsub';
import awsconfig from './aws-exports';
API.configure(awsconfig);
PubSub.configure(awsconfig);

const reducers = combineReducers({
  venues: venuesReducer,
  menu: menuReducer,
  map: mapReducer,
  basket: basketReducer,
  postcode: postcodeReducer,
  center: centerReducer,
  user_loc: userLocationReducer,
  search_obj: searchReducer
});

let basket_template = {
  total: 0.00,
  items: {},
  venue: -1,
  venueid: -1,
  typeid: -1,
  venue_stripe_acct: ""
}

let base_search = {
  "query": "",
  "pricemin": 0,
  "pricemax": 3,
  "latitude": 51.4988,
  "longitude": -0.1749,
  "radius": 2,
  "restaurants": true,
  "bars": true,
  "cafes": true
}

const initialState = {
  venues: [],
  menu: {},
  map: false,
  basket: basket_template,
  postcode: "SW7 2AZ",
  center: [-0.1749, 51.4988],
  user_loc: [],
  search_obj: base_search
};


// const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
// const middlewares = composeEnhancers(applyMiddleware(reduxPromise, logger));
const middlewares = applyMiddleware(reduxPromise, logger);

import Router from './router'

const Location = lazy(() => import('./location'));

import Loader from './loader'

const root = document.getElementById('root');
if (root) {
  ReactDOM.render(
    <Suspense fallback={<Loader/>}>
      <Provider store={createStore(reducers, initialState, middlewares)}>
        <Location />
        <Router />
      </Provider>
    </Suspense>
    ,root);
}

