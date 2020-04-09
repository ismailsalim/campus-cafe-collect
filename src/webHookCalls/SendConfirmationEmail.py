import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decimal import Decimal
import stripe

MY_ADDRESS = 'restaurant.msc@gmail.com'
PASSWORD = 'vmzajfcmltytlqdh'
stripe.api_key = "sk_test_MPd2vPMcOQb0TIqTG0qDiYs900fbJyaxW0"

def send_confirmation_email(event):
    # email_address, receipt_number, restaurant_name, amount
    #print(event)

    email_address = get_customer_email(event)
    #email_address = event['data']['object']['customer_email']
    
    id_number = event['data']['object']['id']
    receipt_number = id_number[-8:]
    restaurant_name = event['data']['object']['metadata']['venue']
    order_amount = calculate_total(event)

    send_email(email_address, receipt_number, restaurant_name, order_amount)

def send_email(email_address, receipt_number, restaurant_name, order_amount):
    # set up the SMTP server   
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.ehlo()
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()       # create a message

    # Prints out the message body for our sake

    decimal_amount = Decimal(order_amount)    
    output = round(decimal_amount,2)
    amount = str(output)
    # setup the parameters of the message
    
    msg['From']=MY_ADDRESS
    msg['To']=email_address
    msg['Subject']="Order Number " + receipt_number
    
    # add in the message body
    message = """\
        <html>
            <body>

                <img src="https://www.tonidigrigio.it/resources/gallery/food-packaging/cover.jpg" alt="Flowers in Chania" width="700" height="300">

                <p><font face="verdana">Thank you for your order.</font></p>

                <h1><font face="verdana">Your order number is {0}.</font></h1>

                <p><font face="verdana">This email is a confirmation of your order at {1} totalling £{2}. </font></p>

                <p><font face="verdana">You may be required to present your order number on collection.</font></p>

            </body>
        </html>
    """
    message = message.format(receipt_number, restaurant_name, amount)
    msg.attach(MIMEText(message, 'html'))
    
    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()

def calculate_total(event):
    processedOrder = event["data"]["object"]["display_items"]
    total = 0
    for product in processedOrder:
        amount = product["amount"] 
        quantity = product["quantity"]
        total += (amount * quantity)
    total = total/100
    return total

def get_customer_email(event):
    customer = stripe.Customer.retrieve(
        event["data"]["object"]["customer"],
        stripe_account = event['data']['object']['metadata']['acct']
         )
    email_address = customer["email"]
    return email_address