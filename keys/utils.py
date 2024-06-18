import random
import string
from django.core.mail import send_mail
from django.utils import timezone


def generate_random_string(length=16):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length)).upper()


def generate_otp(user):
    from .models import OTP
    otp_code = '{:06d}'.format(random.randint(0, 999999))
    OTP.objects.update_or_create(
        user=user,
        defaults={
            'otp_code': otp_code,
            'created_at': timezone.now(),
            'is_used':False
        }
    )
    return otp_code

def send_otp_via_email(user, otp_code):
    otp_code = generate_otp(user)
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp_code}. It will expire in 2 minutes.'
    from_email = 'selormatsu5@example.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

