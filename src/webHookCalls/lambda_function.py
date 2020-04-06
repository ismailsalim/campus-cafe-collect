import json
import stripe
from django.http import HttpResponse
from PushOrderHandler import PushOrderHandler
from DBConnection import DynamoConn
from SendConfirmationEmail import send_confirmation_email

#Using Django
#@csrf_exempt

stripe.api_key = "sk_test_MPd2vPMcOQb0TIqTG0qDiYs900fbJyaxW0"

def lambda_handler(event, context):
    data = event['body']
    json_acceptable_string = data.replace("'","\"")
    input = json.loads(json_acceptable_string)

    event_pi = None

    try:
        event_pi = stripe.Event.construct_from(
        input, stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event_pi.type == 'checkout.session.completed': 
        # Success
        payment_intent = event_pi.data.object    # Not sure if needed     
        conn = DynamoConn('Credentials')
        handler = PushOrderHandler(conn)

        handler_response = handler.handle_request(input, context)
        send_confirmation_email(input)

        return handler_response

    else:
        # Unexpected event type
        return HttpResponse(status=400)

    return HttpResponse(status=200)
