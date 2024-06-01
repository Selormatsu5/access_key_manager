import random
import string

def generate_random_string(length=16):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length)).upper()
