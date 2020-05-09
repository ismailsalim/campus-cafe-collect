# Group 11
**Members:** Ismail Salim, Hamish Hall, Jamal Afzali, Bogdan Cristal, Alberto Marzetta
## Project Title: Application Integration for Restaurant Apps

## Supervisor: Dr. Thomas Heinis

## Application URL
To use the application, open [this link](http://production.dolxjcfav4ei2.amplifyapp.com) in any browser.

### Best Use Of Application 
**On landing,** enter the postcode **SW7 2AZ** to find restaurants that we have simulated.

**To make a payment,** enter the following card details:

*Name:* Anything

*Card Number:* 4242 4242 4242 4242

*Expiry Date:* Any future date

*CVC:* 123

**To retrieve order confirmation,** enter any valid email address.

### Run Application Locally
Run commands (1) and either  (2a) or (2b) in ```/frontend/restaurant-app-react/```:
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

## Frontend Tests
To obtain the front-end test results, run:
```bash
./frontend/restaurant-app-react/node_modules/.bin/jest
```

## Backend Tests

We recommend creating a new environment to avoid any unforseen issues.

To install the dependencies, run in ```/backend/src```:
```bash
pip install -r requirements.txt
```

To obtain the statement coverage, run in ```/backend/src```:
```bash
coverage run -m unittest discover tests
coverage html
```

To obtain the branch coverage, run in ```/backend/src```:
```bash
coverage run --branch -m unittest discover tests
coverage html
```

The respective HTML file will be called index.html and will be in the newly created htmlcov folder.
