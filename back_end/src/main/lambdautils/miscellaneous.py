miscellaneous = {
    'confirmationEmail' : {
        'senderEmail' : 'restaurant.msc@gmail.com',
        'senderPassword': 'vmzajfcmltytlqdh',
        'confirmationMessageTemplate': """\
        <html>
            <body>
                <img src="https://www.tonidigrigio.it/resources/gallery/food-packaging/cover.jpg" \
                alt="Flowers in Chania" width="700" height="300">
                <p><font face="verdana">Thank you for your order.</font></p>
                <h1><font face="verdana">Your order number is {0}.</font></h1>
                <p><font face="verdana">This email is a confirmation of your order at {1} totalling £{2}. </font></p>
                <p><font face="verdana">You may be required to present your order number on collection.</font></p>
            </body>
        </html>
    """
    },
    'stripeAPIkey': "sk_test_MPd2vPMcOQb0TIqTG0qDiYs900fbJyaxW0"
}