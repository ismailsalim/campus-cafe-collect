import React, {Component} from 'react'
import ReactMapboxGl, { Layer, Feature, Marker, Popup } from 'react-mapbox-gl';

import Venue from '../home/venue'

class MapFeatures extends Component {
  constructor(props) {
    super(props)
    this.state = {
      showPopup: false,
      coords:[-0.1749, 51.4988],
      venue: {imgurl: "", name: "", desc: "", logourl: ""}
    }
  }

  openPopUp = (venue) => {
    this.setState({
      showPopup: true,
      coords: [venue.longitude, venue.latitude],
      venue: venue

    })
  }

  closePopUp = () => {
    this.setState({showPopup: false})
  }


  render() {

    return (
      <div>
        {
          this.props.venues.map((venue) => {
            return (
              <Marker
                coordinates={[venue.longitude, venue.latitude]}
                className="marker"

                onMouseEnter={() => this.openPopUp(venue)}
                onMouseLeave={this.closePopUp}
                key={venue.name}
              >

              </Marker>
            )
          })
        }
        {this.state.showPopup && (

          <Popup coordinates={this.state.coords}>
            <Venue venue={this.state.venue} />
          </Popup>

        )}
      </div>

    )
  }
}

export default MapFeatures
