import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
coinpayment_api = settings.COINPAYMENT_API
