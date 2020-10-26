import React, { Component } from 'react'
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import PayButton from './pay_button'

class Checkout extends Component {

  getItems = (regional_curr) => {
    let items =  Object.keys(this.props.basket.items).map((item) => {
      return(
        {
          name: item,
          amount: this.props.basket.items[item].price * 100,
          quantity: this.props.basket.items[item].num,
          currency: regional_curr
        }
      )
    })

    // items[0]["description"] = this.props.basket.venue
    return items
  }


  render() {
    let base_url = "https://production.dolxjcfav4ei2.amplifyapp.com"


    return (
      <div>

        <PayButton
          stripePublicKey={"pk_test_ETk8rfAJNbrGGITQTWn9J90P00lMf7VhSa"}
          apiName="stripe"
          apiEndpoint="/checkout"
          items={this.getItems('gbp')}
          venue={this.props.basket.venue}
          venueid={this.props.basket.venueid}
          typeid={this.props.basket.typeid}
          connectedAccount={this.props.basket.venue_stripe_acct}
          amount={this.props.basket.total}
          success_url={`${base_url}/success?session_id={CHECKOUT_SESSION_ID}&acct=${this.props.basket.venue_stripe_acct}`}
          cancel_url={`${base_url}${this.props.link_loc}`}

          classname={this.props.classname}
          comp={this.props.comp}
          disabled={this.props.disabled}


        />

      </div>
    )
  }
}

function mapStateToProps(state) {
  return {basket: state.basket}
}

export default connect(mapStateToProps, null, null, {
    pure: false,
  })(Checkout);
