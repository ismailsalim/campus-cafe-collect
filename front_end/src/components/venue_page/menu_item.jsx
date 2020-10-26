import React, { Component } from 'react'
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import { Link } from 'react-router-dom';
import { TiPlus } from "react-icons/ti";
import { TiPlusOutline } from "react-icons/ti";
import { TiMinus } from "react-icons/ti";
import { TiMinusOutline } from "react-icons/ti";

import { addToBasket } from '../../actions'
import { removeFromBasket } from '../../actions'
import { emptyBasket } from '../../actions'

import PropTypes from 'prop-types';

class MenuItem extends Component {
  constructor() {
      super();
      this.state = {
        value: 0,
        modal: false
      };
  }

  incrementValue = () => {
    if (this.props.basket.venue == -1 || this.props.basket.venue == this.props.venue.name) {
      this.setState({value: this.state.value + 1})
      this.props.addToBasket({name: this.props.name, price: this.props.price, venue: this.props.venue.name, venueid: this.props.venue.venueid, typeid: this.props.venue.typeid, stripe_acct: this.props.venue.stripeid})
    } else {
      this.setState({modal: true})
    }

  }

  decrementValue = () => {
    if (this.state.value > 0) {
      this.setState({value: this.state.value - 1})
      this.props.removeFromBasket({name: this.props.name, price: this.props.price, venue: this.props.name})
    }
  }

  componentDidMount() {
    if (this.props.basket.items[this.props.name] && this.props.venue.name == this.props.basket.venue) {
      this.setState({value: this.props.basket.items[this.props.name].num})
    }
  }

  toggle = () => {
    this.setState({modal: false})
  }

  clearBasket = () => {
    this.props.emptyBasket()
    this.setState({value: this.state.value + 1})
    this.props.addToBasket({name: this.props.name, price: this.props.price, venue: this.props.venue.name, venueid: this.props.venue.venueid, typeid: this.props.venue.typeid, stripe_acct: this.props.venue.stripeid})
    this.setState({modal: false})
  }

  render() {
    let minus_classes = "price-toggle price-grey"
    if (this.state.value != 0) {
      minus_classes += " price-btns"
    }

    return (
      <div>
        <div className="menu-item">
          <div className="menu-item-left">
            <div className="" key={this.props.name}><span className="item-name">{`${this.props.name}:`}</span><span className="price-bold">{`£${this.props.price.toFixed(2)}`}</span></div>
          </div>
          <div className="menu-item-right">
            <TiMinusOutline className={minus_classes} onClick={this.decrementValue}/>
            <div className="price-toggle">{this.state.value}</div>
            <TiPlusOutline className="price-toggle price-btns" onClick={this.incrementValue}/>
          </div>
        </div>
        <Modal isOpen={this.state.modal} toggle={this.toggle} className={""}>
          <ModalHeader toggle={this.toggle}>Start new order?</ModalHeader>
          <ModalBody>
            {`You have an open order with ${this.props.basket.venue} - would you like to overwrite it?`}
          </ModalBody>
          <ModalFooter>
            <Button color="primary" onClick={this.clearBasket}>Yes</Button>{' '}
            <Button color="secondary" onClick={this.toggle}>Cancel</Button>
          </ModalFooter>
        </Modal>
      </div>
    );
  }
}

MenuItem.propTypes = {
  name: PropTypes.string.isRequired,
  price: PropTypes.number.isRequired

}

function mapStateToProps(state) {
  return {basket: state.basket}
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(
    {addToBasket: addToBasket, removeFromBasket: removeFromBasket, emptyBasket: emptyBasket },
     dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(MenuItem);


