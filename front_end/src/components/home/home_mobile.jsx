import React, { Component, lazy, Suspense } from 'react'
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';


import VenuesContainer from './venues_container'
const MapBox = lazy(() => import('../map/map_box'));

import Loader from '../loader'
import Loader2 from '../loader2'

class HomeMobile extends Component {


  render() {
    let mobile_venues_classes = ""
    let mobile_map_classes = ""

    if (this.props.map_state) {
      mobile_venues_classes += "mobile-off"
      mobile_map_classes += "mobile-on"
    } else {
      mobile_map_classes += "mobile-off"
      mobile_venues_classes += "mobile-on"
    }


    return (

      <div className="home-mobile">
        <div className={mobile_venues_classes}>
          <VenuesContainer/>
        </div>
        <div className={mobile_map_classes}>
          <Suspense fallback={<Loader2/>}>
            <MapBox venues={this.props.venues || []} center={this.props.center} zoom={(this.props.center == [0,0]) ? [0] : [16]}/>
          </Suspense>
        </div>
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
    map_state: state.map,
    venues: state.venues,
    center: state.center
  };
}

HomeMobile.propTypes = {
  map_state: PropTypes.bool.isRequired
}


export default connect(mapStateToProps, null)(HomeMobile);
