# Application Integration for Restaurant Apps
# Group 11
## Group Members
Ismail Salim, Hamish Hall. Jamal Afzali, Bogdan Cristal, Alberto Marzetta

## Application URL:
http://production.dolxjcfav4ei2.amplifyapp.com

Postcode with registered venues:
SW7 2AZ

To process a payment:
Enter the following card details:
Name: Anything
Card Number: 4242 4242 4242 4242
Expiry Date: Any future date
CVC: Any

To retrieve order confirmation:
Enter valid email

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

## To run the backends tests:
To execute coverage tool, enter the following commands from the directory's root:
Statements: coverage run -m unittest discover tests
Branches: coverage run --branch -m unittest discover tests
