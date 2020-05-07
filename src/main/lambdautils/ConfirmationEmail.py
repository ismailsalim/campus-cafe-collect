from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from main.lambdautils.miscellaneous import miscellaneous
import smtplib
import stripe


class ConfirmationEmail:
    """
    class to send confirmation emails
    (could have an abstract emailsender baseclass, to set up later if we need other senders)
    """

    def __init__(self, order) -> None:
        self.order = order
        self.sender = miscellaneous['confirmationEmail']['senderEmail']
        self.password = miscellaneous['confirmationEmail']['senderPassword']
        self.messageTemplate = miscellaneous['confirmationEmail']['confirmationMessageTemplate']

    def sendConfirmation(self) -> None:
        customerEmail = self.getCustomerEmail()
        receiptNumber = self.order['data']['object']['id'][-8:]
        restaurantName = self.order['data']['object']['metadata']['venue']
        orderPrice = self.calculateTotal()
        message = self.messageTemplate.format(receiptNumber, restaurantName, "{:.2f}".format(orderPrice))

        email = MIMEMultipart()
        email['From'] = self.sender
        email['To'] = customerEmail
        email['Subject'] = "Order Number " + receiptNumber
        email.attach(MIMEText(message, 'html'))

        connection = smtplib.SMTP(host='smtp.gmail.com', port=587)
        connection.ehlo()
        connection.starttls()
        connection.login(self.sender, self.password)
        connection.send_message(email)
        connection.quit()

    def calculateTotal(self) -> int:
        items = self.order["data"]["object"]["display_items"]
        total = 0
        for product in items:
            price = product['amount']
            quantity = product["quantity"]
            total += (price * quantity)
        total /= 100
        return total

    def getCustomerEmail(self) -> str:
        customer = stripe.Customer.retrieve(
            self.order["data"]["object"]["customer"],
            stripe_account=self.order['data']['object']['metadata']['acct']
        )
        return customer['email']
