import random
from captcha import VERSION
from captcha.settings import api_settings

cache_template = api_settings.CAPTCHA_CACHE_KEY


def get_cache_key(captcha_key):
    cache_key = cache_template.format(key=captcha_key, version=VERSION.major)
    return cache_key


def random_char_challenge(length):
    chars = "ABCEDFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    ret = ''
    for i in range(length):
        ret += random.choice(chars)
    return ret