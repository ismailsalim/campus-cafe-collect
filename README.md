# Group 11
**Members:** Ismail Salim, Hamish Hall. Jamal Afzali, Bogdan Cristal, Alberto Marzetta
# Title: Application Integration for Restaurant Apps

## Application URL
To use the application, open [this link](http://production.dolxjcfav4ei2.amplifyapp.com) in any browser.

## Best use of the application
On landing, enter the postcode **SW7 2AZ** to find restaurants that we have simulated.

To make a payment, enter the following card details...

*Name:* Anything

*Card Number:* 4242 4242 4242 4242

*Expiry Date:* Any future date

*CVC:* 123

### To retrieve order confirmation:
Enter any valid email address

## To run the frontend locally:
Enter the following commands in the terminal

1. Pre-build: 
```bash
yarn install
```

2a. To run the development build:
```bash
yarn start
```

2b. To run the production build:
```bash
yarn build
```

## To run the frontend test suite
Enter the following command frontend/restaurant-app-react
```bash
./node_modules/.bin/jest
```

## Backend Test Coverage:
In the root directory, execute the following commansds...

For statement coverage
```bash
coverage run -m unittest discover tests
```
For branch coverage
```bash
coverage run --branch -m unittest discover tests
```
