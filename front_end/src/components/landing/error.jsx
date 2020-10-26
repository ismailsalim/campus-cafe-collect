import React, { Component } from 'react'
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import {Link} from 'react-router-dom'
import { Redirect } from 'react-router';

import { postPostcode } from '../../actions'
import { setCenter } from '../../actions'
import { updateSearch } from '../../actions'

class ErrorPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      width: window.innerWidth,
    };
  }


  handleWindowSizeChange = () => {
      this.setState({ width: window.innerWidth });
  };

  handleClick = () => {
    this.setState({redirect: true});
  }


  render() {
    const { width } = this.state;
    const isMobile = width <= 600;
    let sectionStyle = {
      width: "100%",
      height: "100%",
      backgroundSize: (isMobile) ? "cover" : "100% 100%",
      backgroundRepeat: 'no-repeat',
      // backgroundImage: "url(https://restaurant-app.s3.eu-west-2.amazonaws.com/New+Project.webp)"
    };

    if (this.state.redirect) {
      return <Redirect push to="/home" />;
    }

    return (

      <div className="landing-page" style={sectionStyle}>
        <div className="landing-box">
          <div className="landing-title">
            Sorry That Page Was Not Found
          </div>
          <div className="landing-button error-page" onClick={this.handleClick}>Back to Home</div>
        </div>
      </div>
    )
  }
}



export default ErrorPage;
