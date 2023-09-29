from django.test import TestCase
# import settings
from mailsend import emails
import requests

api_key = "mlsn.86d8164114d61a31b62b92a91f75148eb5e795501fd9415ef6802f2a2fd0cb6b"

mailer = emails.NewEmail(api_key)

# define an empty dict to populate with mail values
mail_body = {}

mail_from = {
    "name": "Kelvin",
    "email": "MS_aJOG7d@africanfoodstoresafari.com",
}

recipients = [
    {
        "name": "Maina",
        "email": "kelvinmaina547@gmail.com",
    }
]

reply_to = [
    {
        "name": "Name",
        "email": "reply@domain.com",
    }
]

mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Hello!", mail_body)
mailer.set_html_content("This is the HTML content", mail_body)
mailer.set_plaintext_content("This is the text content", mail_body)
mailer.set_reply_to(reply_to, mail_body)

# using print() will also return status code and data
mailer.send(mail_body)