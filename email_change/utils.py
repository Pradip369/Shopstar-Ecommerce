import random
import hashlib
from django.contrib.auth.tokens import default_token_generator


def generate_key(user, email):
    return hashlib.sha1(bytes(
    default_token_generator.make_token(user) + email + str(random.random()),
    'utf-8',
    )).hexdigest()