import { add_item } from '../basket'
import { remove_item } from '../basket'

const empty_basket = {
  venue: -1,
  total: 0.00,
  items: {}
}

const test_item = {name: 'pizza', price: 15.99}

//need to work around JS immutabiltiy, or redux will not recognize the change

test('empty item does not update basket', () => {
  expect(add_item(empty_basket, {})).toStrictEqual(empty_basket);
})

test("basket items increments with added item", () => {
  const empty_basket = {
    venue: -1,
    total: 0.00,
    items: {}
  }

  const test_item = {name: 'pizza', price: 15.99}
  let basket = add_item(empty_basket, test_item)
  expect(Object.keys(basket.items).length).toBe(1);
})

test("item added into basket['items'] as key", () => {
  const empty_basket = {
    venue: -1,
    total: 0.00,
    items: {}
  }

  const test_item = {name: 'pizza', price: 15.99}
  let basket = add_item(empty_basket, test_item)
  expect(basket.items).toStrictEqual({pizza: {price: 15.99, num: 1}});
})

test("total should increment appropriately", () => {
  const empty_basket = {
    venue: -1,
    total: 0.00,
    items: {}
  }

  const test_item = {name: 'pizza', price: 15.99}
  let basket = add_item(empty_basket, test_item)
  expect(basket.total).toBe(15.99);
})


test("if item already in basket, its number is incremented", () => {
  const empty_basket = {
    venue: -1,
    total: 0.00,
    items: {}
  }

  const test_item = {name: 'pizza', price: 15.99}
  let basket = add_item(empty_basket, test_item)
  basket = add_item(basket, test_item)
  expect(basket.items['pizza'].num).toBe(2);
})

test("if item already in basket, size of basket[items] doesnt change", () => {
  const empty_basket = {
    venue: -1,
    total: 0.00,
    items: {}
  }

  const test_item = {name: 'pizza', price: 15.99}
  let basket = add_item(empty_basket, test_item)
  basket = add_item(basket, test_item)
  expect(Object.keys(basket.items).length).toBe(1);
})


const test_item2 = {name: 'burger', price: 9.99, venue: 2}
test("a new item, is a new entry in basket['items']", () => {
  const empty_basket = {
    venue: -1,
    total: 0.00,
    items: {}
  }

  const test_item = {name: 'pizza', price: 15.99}
  let basket = add_item(empty_basket, test_item)
  basket = add_item(basket, test_item2)
  expect(Object.keys(basket.items).length).toBe(2);
})

// ---------------------------------------------------------------------------//
//REMOVING ITEMS

test("remove an item from empty basket does nothing", () => {
  const empty_basket = {
    venue: -1,
    total: 0.00,
    items: {}
  }
  const test_item = {name: 'pizza', price: 15.99}
  expect(remove_item(empty_basket, test_item)).toStrictEqual(empty_basket);
})

test("remove an item decrements its count", () => {
  const empty_basket = {
    venue: -1,
    total: 0.00,
    items: {}
  }
  const test_item = {name: 'pizza', price: 15.99}
  let basket = add_item(empty_basket, test_item)
  basket = add_item(basket, test_item) // add a second pizza
  basket = remove_item(basket, {name: 'pizza', price: 15.99})
  expect(basket.items['pizza'].num).toStrictEqual(1);
})

test("remove an item decrements total", () => {
  const empty_basket = {
    venue: -1,
    total: 0.00,
    items: {}
  }
  const test_item = {name: 'pizza', price: 15.99}
  let basket = add_item(empty_basket, test_item)
  basket = add_item(basket, test_item) // add a second pizza
  basket = remove_item(basket, {name: 'pizza', price: 15.99})
  expect(basket.total).toStrictEqual(15.99);
})

test("remove an item that isnt in basket does nothing", () => {
  const empty_basket = {
    venue: -1,
    total: 0.00,
    items: {}
  }
  const test_item = {name: 'pizza', price: 15.99}
  expect(remove_item(empty_basket, {name: 'sandwich', price: 3.99})).toStrictEqual(empty_basket);
})

test("removing last instance of item, removes item altogether", () => {
  const empty_basket = {
    venue: -1,
    total: 0.00,
    items: {}
  }
  const test_item = {name: 'pizza', price: 15.99}
  let basket = add_item(empty_basket, test_item)
  basket = remove_item(basket, {name: 'pizza', price: 15.99})
  expect(Object.keys(basket.items).length).toStrictEqual(0);
})










