import React, { Component } from 'react'
import { Elements, StripeProvider } from 'react-stripe-elements';

import PayButtonContent from './pay_button_content'

import PropTypes from 'prop-types';

class PayButton extends Component {
  constructor(props) {
    super(props);
    this.state = {stripe: null};
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.props.connectedAccount && this.props.connectedAccount != prevProps.connectedAccount) {

      if (window.Stripe) {
        this.setState({stripe: window.Stripe(this.props.stripePublicKey, {stripeAccount: this.props.connectedAccount})});
      } else {
        document.querySelector('#stripe-js').addEventListener('load', () => {
          // Create Stripe instance once Stripe.js loads
          this.setState({stripe: window.Stripe(this.props.stripePublicKey, {stripeAccount: this.props.connectedAccount})});
        });
      }
    }
  }

  render() {
    return (
      <StripeProvider stripe={this.state.stripe}>
          <Elements>
              <PayButtonContent
                  apiName={this.props.apiName}
                  apiEndpoint={this.props.apiEndpoint}
                  items={this.props.items}
                  venue={this.props.venue}
                  venueid={this.props.venueid}
                  typeid={this.props.typeid}
                  connectedAccount={this.props.connectedAccount}
                  amount={this.props.amount}
                  success_url={this.props.success_url}
                  cancel_url={this.props.cancel_url}
                  onClick={this.onClickPay}
                  onFail={this.onPayFail}
                  classname={this.props.classname}
                  comp={this.props.comp}
                  disabled={this.props.disabled}
              />
          </Elements>
      </StripeProvider>
    )


  }

};

// PayButton.propTypes = {
//     stripePublicKey: PropTypes.string.isRequired,
//     apiName: PropTypes.string.isRequired,
//     apiEndpoint: PropTypes.string.isRequired,
//     name: PropTypes.string.isRequired,
//     description: PropTypes.string.isRequired,
//     images: PropTypes.array.isRequired,
//     amount: PropTypes.number.isRequired,
//     currency: PropTypes.string.isRequired,
//     quantity: PropTypes.number.isRequired,
//     success_url: PropTypes.string.isRequired,
//     cancel_url: PropTypes.string.isRequired,
// };

export default PayButton;
