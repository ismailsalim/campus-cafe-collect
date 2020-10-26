import React, { Component, lazy, Suspense } from 'react'
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import VenuesContainer from './venues_container'

const MapBox = lazy(() => import('../map/map_box'));

import Loader from '../loader'
import Loader2 from '../loader2'

class HomeDesktop extends Component {


  render() {
    let map_classes = ""
    if (this.props.map_state) {
      map_classes += "map-open"
    } else {
      map_classes += "map-closed"
    }


    return (

      <div className="home-desktop">
        <VenuesContainer/>
        <div className={map_classes}>
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

HomeDesktop.propTypes = {
  map_state: PropTypes.bool.isRequired
}

export default connect(mapStateToProps, null)(HomeDesktop);
