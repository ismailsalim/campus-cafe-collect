import React, { Component } from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { updateSearch } from '../../actions'
import { setVenues } from '../../actions'
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';
import { withStyles } from "@material-ui/core/styles";

const useStyles = () => ({
  root: {
    width: 150,
    color: '#162AF4',
  },
  thumb: {
    height: 28,
    width: 28,
    backgroundColor: '#162AF4'
  }
});

const marks = [
  {
    value: 0,
    label: '£',
  },
  {
    value: 1,
    label: '££',
  },
  {
    value: 2,
    label: '£££',
  },
  {
    value: 3,
    label: '££££',
  }
];


class RangeSlider extends Component {
  constructor(props) {
    super(props)
    this.state = {
      value: [0, 3]
    };

  }

  componentDidMount() {
    this.setState({value: [this.props.search_obj.pricemin, this.props.search_obj.pricemax]})
  }

  handleChange = (event, newValue) => {
    if (newValue != this.state.value) {
      this.setState({value: newValue})
    }
  };

  handleChangeCommitted = (event, newValue) => {
    let newSearch = {...this.props.search_obj}
    newSearch.pricemin = this.state.value[0]
    newSearch.pricemax = this.state.value[1]
    this.props.setVenues(newSearch)
    this.props.updateSearch(newSearch)
  };


  valuetext = (value) => {
    let str = ""
    for (let i = 0 ; i < value ; i++) {
      str += "£"
    }
    return `${str}`;
  }

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <Slider
          value={this.state.value}
          onChange={this.handleChange}
          onChangeCommitted={this.handleChangeCommitted}
          valueLabelDisplay="auto"
          aria-labelledby="range-slider"
          getAriaLabel={this.valuetext}
          valueLabelFormat={this.valuetext}
          getAriaValueText={this.valuetext}
          valueLabelDisplay="auto"
          defaultValue={[0, 3]}
          step={1}
          marks
          min={0}
          max={3}
        />
      </div>
    );

  }


}

function mapStateToProps(state) {
  return {
    search_obj: state.search_obj
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(
    {updateSearch: updateSearch, setVenues: setVenues },
     dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(withStyles(useStyles)(RangeSlider));
