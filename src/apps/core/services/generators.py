import secrets
import binascii
import os
import random
import string
from django.template.defaultfilters import slugify


def generate_random_string(instance_id, length: int):
    generated = ''.join(random.choices(string.ascii_lowercase, k=length))
    result = f"{instance_id}_{generated}"
    return result[:length]


def generate_random_code_4(instance_id):
    random_number = '123456789'
    generated = ''.join(secrets.choice(random_number) for i in range(5))
    result = f"{instance_id}{generated}"
    return int(result[:4])


def generate_random_sms_code_6(instance_id):
    random_number = '123456789'
    generated = ''.join(secrets.choice(random_number) for i in range(7))
    result = f"{instance_id}{generated}"
    return int(result[:6])


def random_activation_sms_code():
    random_number = '123456789'
    generated = ''.join(secrets.choice(random_number) for i in range(6))
    return generated


def generate_otp_auth_key():
    return binascii.hexlify(os.urandom(20)).decode()


def generate_model_slug(field: str, model):
    i = 1
    slug = slugify(field).lower()
    while model.objects.filter(slug=slug).exists():
        slug += str(i)
        i += 1
    return slug


def product_id_generator():
    prefix = 'A'
    random_number = '123456789'
    order_id = ''.join(secrets.choice(random_number) for i in range(5))
    return f"{prefix}-{order_id}"


def invoice_id_generator(instance_id) -> str:
    # 6277473
    random_number = '123456789'
    random_no = ''.join(secrets.choice(random_number) for i in range(3))
    return f'{instance_id}{random_no}'


def credit_unique_id_generator(instance_id) -> str:
    # 6277473
    random_number = '123456789'
    random_no = ''.join(secrets.choice(random_number) for i in range(3))
    return f'{instance_id}{random_no}'


def generate_phone(instance_id):
    """
    +998 90 123 45 67
    +99890 1234567
    """
    random_number = '1234567890'
    generated = ''.join(secrets.choice(random_number) for i in range(7))
    result = f"+99890{instance_id}{generated}"
    return result[:13]
