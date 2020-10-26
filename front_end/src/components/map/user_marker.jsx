import React, {Component} from 'react'
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import ReactMapboxGl, { Layer, Feature, Marker, Popup } from 'react-mapbox-gl';


class UserMarker extends Component {

  render() {

    if (this.props.user_loc.length > 0 ) {
      return (
        <Marker
            coordinates={[this.props.user_loc[0], this.props.user_loc[1]]}
            className=""
        >
          <div className="user-location"></div>
        </Marker>


      )
    }

    return (
      <div></div>
    )

  }
}

function mapStateToProps(state) {
  return {
    user_loc: state.user_loc
  };
}

export default connect(mapStateToProps, null)(UserMarker);

