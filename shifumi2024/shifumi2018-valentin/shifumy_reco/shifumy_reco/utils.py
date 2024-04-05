"""
Utils for gesture recognition part
"""
import random
import string


def str_id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
