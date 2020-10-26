import React, { Component, lazy, Suspense } from 'react'
import {withRouter} from 'react-router-dom';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { API } from 'aws-amplify';
import { IoMdCheckmarkCircleOutline } from "react-icons/io";

import { fetchVenue } from '../../actions';

const MapBox = lazy(() => import('../map/map_box'));

import Loader from '../loader'


class Success extends Component {
  constructor(props) {
    super(props)
    this.state = {
      session: null
    };
  }

  getSession = async() => {
    let split1 = this.props.location.search.split("session_id=")[1]
    let split2 = split1.split("&acct=")
    let token = split2[0]
    let acct = split2[1]
    const body = {token: token, acct: acct}
    // Make the request
    return await API.post('stripe', '/session', { body });
  }

  componentDidMount() {
    let split1 = this.props.location.search.split("session_id=")[1]
    let split2 = split1.split("&acct=")
    let token = split2[0]
    let acct = split2[1]
    console.log(token)
    console.log(acct)
    this.getSession().then(response => {
      console.log(response)
      this.setState({session: response.session})
      this.props.fetchVenue(this.state.session.metadata.venueid, this.state.session.metadata.typeid)
    })



  }

  sumTotal = () => {
    let total = 0
    this.state.session.display_items.map((item) => {
      total += item.amount * item.quantity
    })
    return parseFloat(Math.round(total) / 100).toFixed(2);
  }

  render() {


    if (!this.state.session || !this.props.venues[0]) {
        return (<div className="loader">
          <div data-v-21dcae14="" className="box" category="animation" text=""><div data-v-21dcae14="" className="bouncingLoader"><div data-v-21dcae14=""></div></div></div>
          </div>
        )
    }

    return (
      <Suspense fallback={<Loader/>}>
      <div className="success-page">
        <div className="sucess-box">
          <h1 className="order-code">Order Code: {this.state.session.id.slice(-8)} </h1>
          <div className="success-box-top">
            <IoMdCheckmarkCircleOutline className="success-icon" />
            <h3 className="paymen">Payment Processed!</h3>
            <h5>{this.state.session.metadata.venue} is preparing your order</h5>
            <h5>A confirmation receipt has been sent to your email</h5>
          </div>
          <div className="success-box-info">
            <ul className="success-list">
              {this.state.session.display_items.map((item) => {
                return(
                  <li className="success-items" key={item.custom.name}>{item.custom.name}, x{item.quantity}</li>
                )
              })}
            </ul>
            <div className="success-total">Total: £{this.sumTotal()}</div>

          </div>
          <div className="success-box-map">
          <Suspense fallback={<Loader/>}>
            <MapBox venues={this.props.venues} center={[this.props.venues[0].longitude, this.props.venues[0].latitude]} zoom={[16]}/>
          </Suspense>
          </div>

        </div>

      </div>
      </Suspense>

    )
  }
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators({ fetchVenue }, dispatch);
}

function mapStateToProps(state) {
  return {venues: state.venues}
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Success));
