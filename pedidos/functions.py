import os
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment

PAYPAL_CLIENT_ID = ''
PAYPAL_CLIENT_SECRET = ''


def get_paypal_client():
    client_id = os.environ["PAYPAL_CLIENT_ID"]
    client_secret = os.environ["PAYPAL_CLIENT_SECRET"]
    mode = os.getenv("PAYPAL_MODE", "sandbox").lower()

    env = LiveEnvironment(client_id, client_secret) if mode == "live" \
        else SandboxEnvironment(client_id, client_secret)

    return PayPalHttpClient(env)
