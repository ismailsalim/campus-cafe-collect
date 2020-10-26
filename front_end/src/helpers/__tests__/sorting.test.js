import { sort_by } from '../sorting'

test('sort by lowest price', () => {
  let venues = [{name: "lowest", pricerank: 1}, {name: "highest", pricerank: 3}, {name: "middle", pricerank: 2}]
  let sorted = sort_by(venues, 'price_low', {})

  expect(sorted[0].pricerank).toBe(1);
})

test('sort by highest price', () => {
  let venues = [{name: "lowest", pricerank: 1}, {name: "highest", pricerank: 3}, {name: "middle", pricerank: 2}]
  let sorted = sort_by(venues, 'price_high', {})

  expect(sorted[0].pricerank).toBe(3);
})


test('sort by distance', () => {
  let venues = [{name: "middle", longitude: -0.177834, latitude: 51.4984}, {name: "lowest", longitude: -0.178241, latitude: 51.500609}, {name: "furthest", longitude: -0.177829, latitude: 51.498717}, {name: "far", longitude: -0.19, latitude: 55}]
  let sorted = sort_by(venues, 'distance', {longitude: -0.2265951, latitude: 51.4968882999999})

  expect(sorted[0].name).toBe("lowest");
})

test('sort by distance ptii', () => {
  let venues = [{name: "middle", longitude: -0.177834, latitude: 51.4984}, {name: "lowest", longitude: -0.178241, latitude: 51.500609}, {name: "furthest", longitude: -0.177829, latitude: 51.498717}, {name: "far", longitude: -0.19, latitude: 55}]
  let sorted = sort_by(venues, 'distance', {longitude: -0.2265951, latitude: 51.4968882999999})
  expect(sorted[3].name).toBe("far");
})
