import React, { Component } from 'react'
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { toggleMap } from '../../actions'
import { toggleFilter } from '../../actions'
import { updateSearch } from '../../actions'
import { setVenues } from '../../actions'
import PropTypes from 'prop-types';

import { GiWalk } from "react-icons/gi";
import { GiTreasureMap } from "react-icons/gi";

import RangeSlider from "./slider"
import SortDropdown from "./dropdown"


class Filters extends Component {
  constructor(props) {
    super(props)
    this.state = {
      width: window.innerWidth,
      // restaurants: true,
      // cafes: true,
      // bars: true,
      // pickup: false
    };

  }

  componentDidMount() {
      window.addEventListener('resize', this.handleWindowSizeChange);
  }

  componentWillUnmount() {
      window.removeEventListener('resize', this.handleWindowSizeChange);
  }

    handleWindowSizeChange = () => {
      this.setState({ width: window.innerWidth });
  };

  toggleMode = () => {
    this.setState({pickup: !this.state.pickup})
  }

  toggleType = (e) => {
      let type = e.target.dataset.type
      let newSearch = {...this.props.search_obj}
      newSearch[type] = !this.props.search_obj[type]
      this.props.setVenues(newSearch)
      this.props.updateSearch(newSearch)

  }

  render() {
    const { width } = this.state;
    const isMobile = width <= 600;
    let top_classes = "filters";
    let row_one_classes = "filters-row-one";
    let row_two_classes = "filters-row-two";
    if (!isMobile) {
      top_classes += " filters-flex";
      row_one_classes += " filters-flex";
    }


    let toggles_classes = "filters-toggle"
    if (isMobile) {
      toggles_classes += " toggles-mobile"
    }


    return (
      <div className={top_classes}>
        <div>
          <div className={row_one_classes}>
            <div className="type-buttons">
              <div onClick={this.toggleType} data-type="restaurants" className={(this.props.search_obj.restaurants) ? "type-button type-selected" : "type-button type-deselected"}>Restaurants</div>
              <div onClick={this.toggleType} data-type="cafes" className={(this.props.search_obj.cafes) ? "type-button type-selected" : " type-button type-deselected"}>Cafes</div>
              <div onClick={this.toggleType} data-type="bars" className={(this.props.search_obj.bars) ? "type-button type-selected" : " type-button type-deselected"}>Bars</div>
            </div>
            <div className="price-slider-cntnr">
              <p className="price-icon">£</p>
              <div className={""}>
                <RangeSlider/>
              </div>
            </div>
          </div>
          <div className={row_two_classes}>
            <p>Sort by: </p>
            <SortDropdown/>
          </div>
        </div>
        <div className={toggles_classes}>

          <div  className={"eatmode-toggle eatmode-deselected"}><GiWalk className="toggle-icon"/> <div>Pick Up</div></div>
          <div className="mapbtn-toggle" id="map-toggle" onClick={this.props.toggleMap}>{(this.props.map_state) ? "List" : "Map"}</div>

        </div>
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
    map_state: state.map, search_obj: state.search_obj
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(
    {toggleMap: toggleMap, toggleFilter: toggleFilter, updateSearch: updateSearch, setVenues: setVenues },
     dispatch);
}

Filters.propTypes = {
  map_state: PropTypes.bool.isRequired
}

export default connect(mapStateToProps, mapDispatchToProps)(Filters);

