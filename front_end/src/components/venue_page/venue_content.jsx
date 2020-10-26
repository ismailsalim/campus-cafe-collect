import React, { Component } from 'react'
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { GiPin } from "react-icons/gi";
import { TiArrowLeftOutline } from "react-icons/ti";



import PropTypes from 'prop-types';

import Menu from './menu'

class VenueContent extends Component {

  distance = (lat1,lon1,lat2,lon2) => {
    let R = 6371; // km (change this constant to get miles)
    let dLat = (lat2-lat1) * Math.PI / 180;
    let dLon = (lon2-lon1) * Math.PI / 180;
    let a = Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(lat1 * Math.PI / 180 ) * Math.cos(lat2 * Math.PI / 180 ) *
      Math.sin(dLon/2) * Math.sin(dLon/2);
    let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    let d = R * c;
    // if (d>1) return Math.round(d)+"km";
    // else if (d<=1) return Math.round(d*1000)+"m";
    return d;
  }

  renderWalkingDistance = () => {
     if (this.props.user_loc.length > 0) {
      let d = this.distance(this.props.user_loc[1], this.props.user_loc[0], this.props.venue.latitude, this.props.venue.longitude)
      return `Distance: ${Math.round(((d / 4) * 60))}min` //walking speed of 5km/hour
    } else {
      return ""
    }
  }

  render() {
    if (this.props.user_loc.length > 0) {
      let d = this.distance(this.props.user_loc[1], this.props.user_loc[0], this.props.venue.latitude, this.props.venue.longitude)

    }
    return (
      <div className="venue-page">
        <Link className="back-button" to="/home">
          <TiArrowLeftOutline/>
          <div>Back</div>
         </Link>
        <div className="venue-item">
          <h3>{this.props.venue.name}</h3>
          <p>{this.props.venue.desc}</p>
          <p className="venue-address"><span className="venue-pin">{<GiPin/>}</span>{this.props.venue.address}</p>
          <div className="times">
            <p>{`Prep time: ${this.props.venue.prep_time}min`}</p>
            <p>{this.renderWalkingDistance()}</p>
          </div>
        </div>
        <div className="venue-menu">
          <Menu venue={this.props.venue}/>
        </div>
      </div> );
  }
}

function mapStateToProps(state) {
  return { user_loc: state.user_loc };
}

VenueContent.propTypes = {
  venue: PropTypes.object.isRequired,
  venue: PropTypes.shape({
    name: PropTypes.string.isRequired,
    desc: PropTypes.string.isRequired,
    address: PropTypes.string.isRequired
  })
}


export default connect(mapStateToProps, null)(VenueContent);
