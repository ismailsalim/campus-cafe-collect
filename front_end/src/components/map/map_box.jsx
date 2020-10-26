import React, {Component} from 'react'
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import ReactMapboxGl, { Layer, Feature, Marker, Popup } from 'react-mapbox-gl';

import MapFeatures from './map_features'
import UserMarker from './user_marker'

class MapBox extends Component {



  render() {
    const Map = ReactMapboxGl({
      accessToken:
        'pk.eyJ1IjoiaGFjaGFsbCIsImEiOiJjazhhY2U5ajkwMHh6M2dwZTZnODg2bXhuIn0.ESQOFjdsmHaRB2xsjobMDQ'
    });


    return (
      <div className={"map-box"}>


      <Map
        style="mapbox://styles/mapbox/light-v9"
        containerStyle={{
          height: '100%',
          minWidth: '100%'
        }}
        zoom={this.props.zoom}
        center={this.props.center}
      >

        <MapFeatures venues={this.props.venues}/>
        <UserMarker />

      </Map>

      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
    map_state: state.map
  };
}

export default connect(mapStateToProps, null)(MapBox);
