import json
import stripe
from django.http import HttpResponse
from PushOrderHandler import PushOrderHandler
from DBConnection import DynamoConn

#Using Django
#@csrf_exempt

def lambda_handler(event, context):
    event_pi = None

    try:
        event_pi = stripe.Event.construct_from(
        event, stripe.api_key
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
        return handler.handle_request(event, context)

    else:
        # Unexpected event type
        return HttpResponse(status=400)

    return HttpResponse(status=200)
