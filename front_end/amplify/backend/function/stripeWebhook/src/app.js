/*
Copyright 2017 - 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
    http://aws.amazon.com/apache2.0/
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
*/

const AWS = require('aws-sdk');

// Stripe parameters
const stripe = require('stripe')(process.env.REACT_APP_STRIPE_PRIVATE_KEY);
const endpointSecret = process.env.REACT_APP_STRIPE_ENDPOINT_SECRET;

const express = require('express');
const bodyParser = require('body-parser');
const awsServerlessExpressMiddleware = require('aws-serverless-express/middleware');

// declare a new express app
const app = express();
// app.use(bodyParser.json());
app.use(awsServerlessExpressMiddleware.eventContext());

// Enable CORS for all methods
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next()
});


app.use((req, res, next) => {
  let data_stream ="";

  // Readable streams emit 'data' events once a listener is added
  req.setEncoding('utf-8')
  .on('data', function(data) {
    data_stream += data;
  })
  .on('end', function() {
    req.rawBody
    req.rawBody = data_stream;
    next();
  })
});


app.post('/webhook', (req, res) => {
  // Add your code here

  const sig = req.headers['stripe-signature'];
  let event;
  try {

     event = stripe.webhooks.constructEvent(req.rawBody, sig, endpointSecret);
     console.log(event);
  }
  catch (err) {
     return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Handle the event
  switch (event.type) {
    case 'checkout.session.completed':
      console.log('Payment checkout session was successful!')
      break;
    default:
      // Unexpected event type
      return res.status(400).end();
  }

  // Return a res to acknowledge receipt of the event
  res.json({ received: true });
});


app.listen(4242, () => console.log('Running on port 4242'));

// Export the app object. When executing the application local this does nothing. However,
// to port it to AWS Lambda we will create a wrapper around that will load the app from
// this file
module.exports = app
