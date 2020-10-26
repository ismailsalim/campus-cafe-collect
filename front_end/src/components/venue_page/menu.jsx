import React, { Component } from 'react'
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import PropTypes from 'prop-types';

import MenuItem from './menu_item';

function isEmpty(obj) {
    for(var prop in obj) {
        if(obj.hasOwnProperty(prop))
            return false;
    }
    return true;
}

class Menu extends Component {

  render() {
    if (isEmpty(this.props.menu)) {
        return (<div className="loader menu-loader">
          <div data-v-21dcae14="" className="box" category="animation" text=""><div data-v-21dcae14="" className="bouncingLoader"><div data-v-21dcae14=""></div></div></div>
          </div>
        )
      }
    return (
      <div className="menu">
        {Object.keys(this.props.menu).map((key, index) => {
            return (
              <div className="manu-section" key={key}>
                <h3 className="menu-title">{key}</h3>
                {this.props.menu[key].map((menu_item) => {
                  return (<MenuItem key={menu_item[1]} name={menu_item[1]} price={menu_item[2]} venue={this.props.venue}/>)
                })}
              </div>
            )
          })}
      </div> );
  }
}

function mapStateToProps(state) {
  return {
    menu: state.menu
  };
}

Menu.propTypes = {
  menu: PropTypes.object.isRequired
}

export default connect(mapStateToProps, null)(Menu);

