import random
import string

def generate_password(length=12, use_symbols=True, use_numbers=True, use_uppercase=True):
    charset = string.ascii_lowercase
    if use_uppercase:
        charset += string.ascii_uppercase
    if use_numbers:
        charset += string.digits
    if use_symbols:
        charset += string.punctuation

    if not charset:
        raise ValueError("No character types selected.")

    return ''.join(random.choice(charset) for _ in range(length))
