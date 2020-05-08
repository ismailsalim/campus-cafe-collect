# Group 11
**Members:** Ismail Salim, Hamish Hall. Jamal Afzali, Bogdan Cristal, Alberto Marzetta
# Project Title: Application Integration for Restaurant Apps

## Application URL
To use the application, open [this link](http://production.dolxjcfav4ei2.amplifyapp.com) in any browser.

## Best use of the application
**On landing,** enter the postcode **SW7 2AZ** to find restaurants that we have simulated.

**To make a payment,** enter the following card details:

*Name:* Anything

*Card Number:* 4242 4242 4242 4242

*Expiry Date:* Any future date

*CVC:* 123

**To retrieve order confirmation,** enter any valid email address.

## To run the frontend locally
Run commands: (1) and either  (2a) or (2b) in ```./frontend/restaurant-app-react/```:
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

3. Site will be hosted at ```localhost:8081```

## Frontend Test Suite
To obtain the front-end test results, run:
```bash
.frontend/restaurant-app-react/node_modules/.bin/jest
```

## Backend Test Coverage
To install the dependencies, run:
```bash
pip install -r requirements.txt
```

To obtain the statement coverage, run:
```bash
coverage run -m unittest discover tests
coverage html
```

To obtain the branch coverage, run:
```bash
coverage run --branch -m unittest discover tests
coverage html
```
