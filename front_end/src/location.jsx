import React, { Component } from 'react'
import { geolocated } from "react-geolocated";
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import {setUserLoc} from "./actions"

class Location extends Component {

  componentDidUpdate(prevProps, prevState) {
    if (!this.props.isGeolocationAvailable) {
      console.log("Browser doesn't support GeoLocation")
    } else if (!this.props.isGeolocationEnabled) {
      console.log("Geolocation is not enabled")
    } else if ( this.props.coords.latitude && this.props.coords.longitude) {
      console.log(`latitude: ${this.props.coords.latitude}, longitude: ${this.props.coords.longitude}`)
      this.props.setUserLoc([this.props.coords.longitude, this.props.coords.latitude])
    } else {
      console.log("Getting location data")
    }

  }

    render() {
      return (<div></div>)
    }
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(
    {setUserLoc: setUserLoc },
     dispatch);
}

export default geolocated({
    positionOptions: {
        enableHighAccuracy: false,
    },
    userDecisionTimeout: 5000,
    watchPosition: true,
})( connect(null, mapDispatchToProps)(Location));
