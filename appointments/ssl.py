import string
import random
from django.contrib.auth.decorators import login_required  
from sslcommerz_lib import SSLCOMMERZ
from .models import PaymentGateWaySettings

def unique_transaction_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def sslcommerz_payment_gateway(request, name, grand_total):
    gateway_auth_details = PaymentGateWaySettings.objects.all().first()
    
    settings = {'store_id': gateway_auth_details.store_id,
                'store_pass': gateway_auth_details.store_pass, 'issandbox': True}
    
    sslcommez = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = grand_total
    post_body['currency'] = "BDT"
    post_body['tran_id'] = unique_transaction_id_generator()
    post_body['success_url'] = ''
    post_body['fail_url'] = ''
    post_body['cancel_url'] = ''
    post_body['emi_option'] = 0
    post_body['cus_email'] = 'request.user.email'  # Retrieve email from the current user session
    post_body['cus_phone'] = "address.phone_number " # Retrieve phone from the current user session
    post_body['cus_add1'] = "address.thana"  # Retrieve address from the current user session
    post_body['cus_city'] = "address.zila"  # Retrieve city from the current user session
    post_body['cus_country'] = 'Bangladesh'
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"

    # OPTIONAL PARAMETERS
    post_body['value_a'] = name

    response = sslcommez.createSession(post_body)
    
    if response.get('status') == 'SUCCESS':
        return f"https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY={response.get('sessionkey')}"
    else:
        raise ValueError(f"Failed to create payment session. Response: {response}")