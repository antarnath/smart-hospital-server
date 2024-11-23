import string
import random
from django.contrib.auth.decorators import login_required  
from sslcommerz_lib import SSLCOMMERZ
from .models import PaymentGateWaySettings

def unique_transaction_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def sslcommerz_payment_gateway(request, user, amount, id, doctor):
    gateway_auth_details = PaymentGateWaySettings.objects.all().first()
    print('===================')
    print(id)
    print('===================')
    
    settings = {'store_id': gateway_auth_details.store_id,
                'store_pass': gateway_auth_details.store_pass, 'issandbox': True}
    
    sslcommez = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = unique_transaction_id_generator()
    post_body['success_url'] = f'http://127.0.0.1:8000/api/v1/appointments/payment/success?id={id}/'
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
    post_body['value_a'] = user
    post_body['value_b'] = amount
    post_body['value_c'] = id
    post_body['value_d'] = doctor

    response = sslcommez.createSession(post_body)
    
    if response.get('status') == 'SUCCESS':
        return f"https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY={response.get('sessionkey')}"
    else:
        raise ValueError(f"Failed to create payment session. Response: {response}")