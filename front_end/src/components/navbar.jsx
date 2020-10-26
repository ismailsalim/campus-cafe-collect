import React, { Component, lazy, Suspense } from 'react'
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import {withRouter} from 'react-router-dom';


import { GiHamburger } from "react-icons/gi";
import { GiShoppingCart } from "react-icons/gi";

const Checkout = lazy(() => import('./basket/checkout'));
const NavBarSearch = lazy(() => import('./navbar_search'));

import Loader from './loader'
import Loader2 from './loader2'

class NavBar extends Component {
  constructor() {
      super();
      this.state = {
        width: window.innerWidth,
      };
    }

    componentDidMount() {
      window.addEventListener('resize', this.handleWindowSizeChange);
    }

    // make sure to remove the listener
    // when the component is not mounted anymore
    componentWillUnmount() {
      window.removeEventListener('resize', this.handleWindowSizeChange);
    }

    handleWindowSizeChange = () => {
      this.setState({ width: window.innerWidth });
  };

  basketComp = () => {
    let basket_classes = "navbar-basket"
    if (this.props.basket.total > 0) {
      basket_classes += " basket-active"
    }
    return (
      <div className={basket_classes}>
        <GiShoppingCart className="nav-basket-icon navbar-icon"/>
        <div className="basket-cost">{`£${this.props.basket.total}`}</div>
      </div>
    )
  }

  getLocation = () => {
    const {pathname} = this.props.location;
    return pathname
  }

  render() {
    const { width } = this.state;
    const isMobile = width <= 600;
    let base = "https://test.dolxjcfav4ei2.amplifyapp.com"

    return (
      <div className="navbarr">
        <div className="navbar-section navbar-left">
          <Link to='/home'>
            <GiHamburger className="navbar-logo navbar-icon"/>
          </Link>
          <Suspense fallback={<Loader2/>}>
            <NavBarSearch/>
          </Suspense>
        </div>
        <div className=" navbar-right">
          {(isMobile) ?
            <div>
              <Suspense fallback={<Loader2/>}>
                <Checkout disabled={this.props.basket.total == 0} link_loc={this.getLocation()} classname="" comp={this.basketComp()}/>
              </Suspense>
            </div>

            :

            <div className="navbar-section">
              <Suspense fallback={<Loader2/>}>
                <Checkout disabled={this.props.basket.total == 0} link_loc={this.getLocation()} classname="" comp={this.basketComp()}/>
              </Suspense>
            </div>


          }

        </div>
      </div>
    )
  }
}


function mapStateToProps(state) {
  return { basket: state.basket };
}

export default withRouter(connect(mapStateToProps, null)(NavBar));
