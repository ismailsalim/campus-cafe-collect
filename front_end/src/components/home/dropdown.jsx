import React, { Component } from 'react';
import { ButtonDropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { setVenues } from '../../actions'
import { sortByPriceLow } from '../../actions'
import { sortByPriceHigh } from '../../actions'
import { sortByDistance } from '../../actions'


class SortDropdown extends Component {
  constructor(props) {
    super(props)
    this.state = {
      open: false
    };

  }

  toggle = () => {
    this.setState({open: !this.state.open})
  };

  distanceRender = () => {
    if (this.props.user_loc.length > 0) {
      return (
        <DropdownItem onClick={this.distanceSort}>Distance</DropdownItem>
      )
    }
  }

  relevanceSort = () => {
    this.props.setVenues()
  }

  priceLowSort = () => {
    this.props.sortByPriceLow()
  }

  priceHighSort = () => {
    this.props.sortByPriceHigh()
  }

  distanceSort = () => {
    this.props.sortByDistance({longitude: this.props.user_loc[0], latitude: this.props.user_loc[1]})
  }

  render() {
    return (
      <ButtonDropdown isOpen={this.state.open} toggle={this.toggle}>
        <DropdownToggle className="sort-by-box" caret>

        </DropdownToggle>
        <DropdownMenu className="dropdown-text">
          <DropdownItem onClick={this.relevanceSort}>Relevance</DropdownItem>
          {this.distanceRender()}
          <DropdownItem onClick={this.priceLowSort}>Price Lowest</DropdownItem>
          <DropdownItem onClick={this.priceHighSort}>Price Highest</DropdownItem>
        </DropdownMenu>
      </ButtonDropdown>
    );

  }
}

function mapStateToProps(state) {
  return {
    user_loc: state.user_loc
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(
    {setVenues: setVenues, sortByPriceLow: sortByPriceLow, sortByPriceHigh: sortByPriceHigh, sortByDistance: sortByDistance },
     dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(SortDropdown);
