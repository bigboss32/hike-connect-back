import random


def generate_email_code():
    return str(random.randint(100000, 999999))
