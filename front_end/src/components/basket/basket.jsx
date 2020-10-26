import React, { Component, lazy, Suspense } from 'react'
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { Link } from 'react-router-dom';
import {withRouter} from 'react-router-dom';

const Checkout = lazy(() => import('./checkout'));

import Loader from '../loader'

class Basket extends Component {

  getLocation = () => {
    const {pathname} = this.props.location;
    return pathname
  }


  render() {

    let classes = "basket"
    classes += (this.props.mobile) ? " basket-mobile" : " basket-desktop"

    if (this.props.basket.total == 0 || this.props.venue != this.props.basket.venue) {
      classes += " basket-close"
    }


    return (
      <Suspense fallback={<Loader/>}>
      <div className={classes}>
        <div className="basket-details">
          <div className="basket-left">Basket:</div>
          <div className="basket-right">{`£${this.props.basket.total.toFixed(2)}`}</div>
        </div>
        <Checkout disabled={false} link_loc={this.getLocation()} classname={"co-button"} comp={<p className="">Go To Checkout</p>}/>
      </div>
      </Suspense>
    )
  }
}

function mapStateToProps(state) {

  return { basket: state.basket };
}

export default withRouter(connect(mapStateToProps, null)(Basket));

