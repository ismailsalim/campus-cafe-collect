from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from main.lambdautils.miscellaneous import miscellaneous
import json
import smtplib


class ConfirmationEmail:
    """
    class to send confirmation emails
    """

    def __init__(self, order, customerEmail) -> None:
        self.order = json.loads(order.replace("'","\""))
        self.sender = miscellaneous['confirmationEmail']['senderEmail']
        self.password = miscellaneous['confirmationEmail']['senderPassword']
        self.messageTemplate = miscellaneous['confirmationEmail']['confirmationMessageTemplate']
        self.customerEmail = customerEmail

    def sendConfirmation(self) -> None:
        receiptNumber = self.order['data']['object']['id'][-8:]
        restaurantName = self.order['data']['object']['metadata']['venue']
        orderPrice = self.calculateTotal()
        message = self.messageTemplate.format(receiptNumber, restaurantName, "{:.2f}".format(orderPrice))

        email = MIMEMultipart()
        email['From'] = self.sender
        email['To'] = self.customerEmail
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