import React, { Component } from 'react'
import StarRatings from 'react-star-ratings';
import PropTypes from 'prop-types';


class Venue extends Component {

  render() {

    return (

      <div className="venue-listing">
        <img src={this.props.venue.imgurl} />
          <div className="card-venue-infos">
            <div>
              <h2>{this.props.venue.name}</h2>
              <p>{this.props.venue.desc}</p>
            </div>
            <h2 className="card-venue-pricing">
              <StarRatings
                rating={this.props.venue.rating}
                starRatedColor="#EEC0DB"
                starEmptyColor="#5D576B"
                numberOfStars={5}
                name='rating'
                starDimension="15px"
                starSpacing="1px"
              />
            </h2>
            <img src={this.props.venue.logourl} className="card-venue-user avatar-bordered" />
          </div>

      </div>
    )
  }
}

Venue.propTypes = {
  venue: PropTypes.object.isRequired,
  venue: PropTypes.shape({
    name: PropTypes.string.isRequired,
    desc: PropTypes.string.isRequired,
    imgurl: PropTypes.string.isRequired,
    logourl: PropTypes.string.isRequired
  })
}


export default Venue;
