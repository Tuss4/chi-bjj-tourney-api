import json
import requests
from django.conf import settings


CONFIRM_EMAIL = """
Hello {0},

Before you can enjoy everything TourneyFinder has to offer,
please confirm your account at the following link:
{1}

Thank you,

Team TourneyFinder
"""

CONFIRM_SUBJECT = "Please Confirm Your TourneyFinder Account"

PASSWORD_RESET_EMAIL = """
Please click the following link to reset your password:

{0}

Thank you,

Team TourneyFinder
"""

PASSWORD_SUBJECT = "TourneyFinder - Reset Your Password"


class TourneyEmail(object):

    def send_confirmation_email(self, user, token):
        body = CONFIRM_EMAIL.format(user.email, token.token)
        return self.send_email(user.email, CONFIRM_SUBJECT, body)

    def send_password_reset(self, user, token):
        body = PASSWORD_RESET_EMAIL.format(token.token)
        return self.send_email(user.email, PASSWORD_SUBJECT, body)

    def send_email(self, to, subject, body_text):
        message = {
            "From": "noreply@tourneyfinder.com",
            "To": to,
            "Subject": subject,
            "TextBody": body_text,
            "TrackOpens": False
        }
        headers = {
            'X-Postmark-Server-Token': settings.POSTMARK_API_TOKEN,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        resp = requests.post(
            settings.POSTMARK_URL,
            headers=headers,
            data=json.dumps(message))
        return resp
