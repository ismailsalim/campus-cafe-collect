import React, { Component } from 'react'
import { API } from 'aws-amplify';
import { injectStripe } from 'react-stripe-elements';
import "regenerator-runtime/runtime.js";
import PropTypes from 'prop-types';


class PayButtonContent extends Component {
  constructor(props) {
    super(props)
    this.state = {
      loading: false
    };
  }

  handlePay = async() => {
    if (!this.props.disabled) {
      const body = {
          items: this.props.items,
          success_url: this.props.success_url,
          cancel_url: this.props.cancel_url,
          metadata: {venue: this.props.venue, venueid: this.props.venueid, typeid: this.props.typeid, acct: this.props.connectedAccount},
          connectedAccount: this.props.connectedAccount
      };
      // Make the request

      const response = await API.post(this.props.apiName, this.props.apiEndpoint, { body });
      // Redirect the user to the checkout session
      console.log(response.session)
      this.props.stripe.redirectToCheckout({
        sessionId: response.session.id
      }).then(function (result) {
        console.log(result.error.message)
      });
    } else {
      console.log("basket is empty")
    }


  };


  render() {
    return (
      <div onClick={this.handlePay} disabled={this.state.loading} className={this.props.classname}>
        {this.props.comp}
      </div>
    )
  }
}



// PayButtonContent.propTypes = {
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

export default injectStripe(PayButtonContent);
