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
