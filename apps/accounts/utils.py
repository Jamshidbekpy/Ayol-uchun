import random
import requests
from django.utils import timezone
from datetime import timedelta
from .models import PhoneVerification
from core.settings.base import ESKIZ_BASE_URL, ESKIZ_EMAIL, ESKIZ_PASSWORD

def get_eskiz_token():
    response = requests.post(f"{ESKIZ_BASE_URL}/auth/login", data={
        "email": ESKIZ_EMAIL,
        "password": ESKIZ_PASSWORD,
    })
    return response.json()["data"]["token"]

def generate_code():
    # Always generate a 6-digit numeric code
    code = str(random.randint(100000, 999999))
    print(code)
    return code

def send_sms_code(phone):
    code = generate_code()
    expires_at = timezone.now() + timedelta(minutes=5)

    # Delete existing codes
    PhoneVerification.objects.filter(phone=phone).delete()

    # Save new code to DB
    PhoneVerification.objects.create(phone=phone, code=code, expires_at=expires_at)

    # Get auth token
    token = get_eskiz_token()

    # Send SMS
    headers = {
        "Authorization": f"Bearer {token}"
    }
    # message = f"Your verification code is: {code}"
    message = "Bu Eskiz dan test"
    phone_number = phone[1:] if phone.startswith("+") else phone
    payload = {
        "mobile_phone": phone_number, # remove + at beginning
        "message": message,
        "from": "4546",  # default sender
        "callback_url": "http://example.com",  # optional
    }
    sms_response = requests.post(f"{ESKIZ_BASE_URL}/message/sms/send", headers=headers, data=payload)

    print(sms_response.json())
def check_code(phone, input_code):
    try:
        record = PhoneVerification.objects.get(phone=phone)
    except PhoneVerification.DoesNotExist:
        return False, "Verification code not found."

    if record.is_expired():
        return False, "Verification code has expired."

    if record.code != input_code:
        return False, "Invalid verification code."

    return True, "Verification successful."


