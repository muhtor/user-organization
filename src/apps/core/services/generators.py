import secrets
import binascii
import os
import uuid
import random
import string


def generate_random_string(instance_id, length: int):
    generated = ''.join(random.choices(string.ascii_lowercase, k=length))
    result = f"{instance_id}_{generated}"
    return result[:length]


def rename_image(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('images/avatar/', new_filename)
