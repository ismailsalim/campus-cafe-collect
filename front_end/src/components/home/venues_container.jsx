import React, { Component, lazy, Suspense } from 'react'
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import {Link} from 'react-router-dom'

import { emptyVenues } from '../../actions';

const VenueList = lazy(() => import('./venue_list'));

import Loader from '../loader'

class VenuesContainer extends Component {

  handleClick = () => {
    this.props.emptyVenues()
  }

  render() {

    return (
      <div className="venues-container">
        <div className="venues-title-container">
          <h2 className="venues-container-title">Venues in <span className="postcode-text">{this.props.postcode}</span></h2>
          <div className="change-postcode">
            <span className="change-bracket">(</span><Link to="/" className="change-link" onClick={this.handleClick}>change</Link><span className="change-bracket">)</span>
          </div>
        </div>
        <Suspense fallback={<Loader/>}>
          <VenueList/>
        </Suspense>
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {postcode: state.postcode}
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(
    {emptyVenues: emptyVenues },
     dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(VenuesContainer);
