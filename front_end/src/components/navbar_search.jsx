import React, { Component } from 'react'
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { FaSistrix } from "react-icons/fa";
import { setVenues } from '../actions'
import { updateSearch } from '../actions'

class NavBarSearch extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: '',
      suggestions: [],
      focus: false,
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({focus: true})
    const ROOT_URL = "https://fncflnxl03.execute-api.eu-west-2.amazonaws.com/testing/get-tags"
    const proxyurl = "https://cors-anywhere.herokuapp.com/"

    if (event.target.value != "") {
      this.setState({value: event.target.value}, () => {
        const promise = fetch(`${proxyurl}${ROOT_URL}/?query=${this.state.value}`, {headers: {'Access-Control-Allow-Origin': '*'}})
        .then(response => response.json())
        .then((data => {
          if (data.response == 404) {
            this.setState({suggestions: []})
          } else {
            this.setState({suggestions: JSON.parse(data.body)})
          }
        }))
      })
    } else {
      this.setState({value: "", suggestions: []})
    }

  }

  handleSubmit(event) {

    this.props.setVenues(this.props.search_obj)
    event.preventDefault();

  }

  handleFocus = () => {
    this.setState({focus: true})
    if (this.state.value == "") {
      this.setState({suggestions: []})
    }
  }

  handleFocusOut = () => {
    this.setState({focus: false})
  }

   BoldedText = (text, shouldBeBold ) => {
    const textArray = text.split(shouldBeBold);
    return (
      <span className="sugg-span">
        {textArray.map((item, index) => (
          <div key={index}>
            {item}
            {index !== textArray.length - 1 && (
              <b>{shouldBeBold}</b>
            )}
          </div>
        ))}
      </span>
    );
  }

  componentDidMount() {
    this.setState({value: this.props.search_obj.query})
  }

  submitWSuggestion = (e) => {
    let q = e.target.dataset.suggestion
    this.setState({value: q, focus: false})
    let newSearch = {...this.props.search_obj}
    newSearch.query = q
    this.props.setVenues(newSearch)
    this.props.updateSearch(newSearch)
  }

  blockDefault = () => {
    event.preventDefault()
  }

  render() {
    return (
      <div className="navsearch-box">
        <form onFocus={this.handleFocus} onBlur={this.handleFocusOut} onSubmit={this.handleSubmit}>

            <input className="nav-searchbar" type="text" placeholder="What are you looking for?" value={this.state.value || ''} onChange={this.handleChange} />
            <button type="submit" className="nav-btn"><FaSistrix className="nav-magnifying"/></button>
          {/*<input type="submit" value="Submit" />*/}
        </form>
        {(this.state.focus && this.state.suggestions.length > 0) ?
          <div className="suggestions">
            {this.state.suggestions.map((sugg) => {
              return (
                <div onClick={this.submitWSuggestion} onMouseDown={this.blockDefault} data-suggestion={sugg[0]} className="suggestion" key={sugg[0]}>
                  <div className="sugg-content">
                    <div className="sugg-item">{this.BoldedText(sugg[0], this.state.value)}</div>
                    <div className="sugg-count">({sugg[1]})</div>
                  </div>
                </div>
              )
            })}
          </div>
          : ""
        }
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {
    map_state: state.map, search_obj: state.search_obj
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(
    {setVenues: setVenues, updateSearch: updateSearch },
     dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(NavBarSearch);
