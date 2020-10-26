/*
Copyright 2017 - 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
    http://aws.amazon.com/apache2.0/
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
*/
const stripe = require('stripe')(process.env.REACT_APP_STRIPE_PRIVATE_KEY);

var express = require('express')
var bodyParser = require('body-parser')
var awsServerlessExpressMiddleware = require('aws-serverless-express/middleware')

// declare a new express app
var app = express()
app.use(bodyParser.json())
app.use(awsServerlessExpressMiddleware.eventContext())

// Enable CORS for all methods
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*")
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
  next()
});


app.post('/checkout', async function (req, res) {
  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      success_url: req.body.success_url,
      cancel_url: req.body.cancel_url,
      metadata: req.body.metadata,
      line_items: req.body.items,
      payment_intent_data: {
        application_fee_amount: 200,
      },

      }, {
        stripeAccount: req.body.connectedAccount,
      });

    res.json({ err: null, success: 'Create stripe checkout session succeed!', session })
  } catch (err) {
    res.json({ err: err })
  }
});




app.listen(3000, function() {
    console.log("App started")
});



// Export the app object. When executing the application local this does nothing. However,
// to port it to AWS Lambda we will create a wrapper around that will load the app from
// this file
module.exports = app;



