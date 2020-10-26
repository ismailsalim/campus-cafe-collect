import React, { Component } from 'react';
import { Container, Row, Col } from 'reactstrap';
import PropTypes from 'prop-types';

import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { setVenues } from '../../actions';
import { updateSearch } from '../../actions';

import Venue from './venue'

class VenueList extends Component {
  constructor(props) {
    super(props)
    this.state = {
      empty: false
    };

  }

  componentDidMount() {
    let newSearch = {...this.props.search_obj}
    newSearch.longitude = this.props.center[0]
    newSearch.latitude = this.props.center[1]
    this.props.setVenues(newSearch);
    this.props.updateSearch(newSearch)

  }


  render() {
    if (this.props.center[0] == 0 && this.props.center[1] == 0) {
      return (
        <div className="invalid-postcode">Invalid Postcode</div>
      )
    }

    if (!this.props.venues) {
      return (
        <div className="invalid-postcode">No matches, try refine your search</div>
      )
    }

    if (this.props.venues.length == 0) {
      return (<div className="loader">
          <div data-v-21dcae14="" className="box" category="animation" text=""><div data-v-21dcae14="" className="bouncingLoader"><div data-v-21dcae14=""></div></div></div>
        </div>
      )
    }

    let card_classes = "venue-card"

    if (this.props.map) {
      card_classes += " card-map-mode"
    }

    return (
      <div>
        <Container>
          <Row>
            {this.props.venues.map((venue) => {
              return (
                <Col xs={12} sm={(this.props.map) ? 12 : 4} key={venue.name}>
                  <Link style={{textDecoration: "none"}} to={`/venues/${venue.venueid}/${venue.typeid}`}>
                    <div className={card_classes}>
                      <Venue key={venue.name} venue={venue}/>
                    </div>
                  </Link>
                </Col>
              )
            })}
          </Row>
        </Container>
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
    venues: state.venues, map: state.map, center: state.center, search_obj: state.search_obj
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(
    {setVenues: setVenues, updateSearch: updateSearch },
     dispatch);
}

VenueList.propTypes = {
  venues: PropTypes.array
}


export default connect(mapStateToProps, mapDispatchToProps)(VenueList);
