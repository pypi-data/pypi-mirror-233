import hashlib

__all__ = [
    'calculate_sign',
]

def calculate_sign(secret_key, data: dict):
    data_str = ''.join(str(value) for value in data.values())
    return hashlib.sha1(str(data_str + secret_key).encode()).hexdigest()
