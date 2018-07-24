import random
from captcha import VERSION
from captcha.conf.settings import api_settings

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


def math_challenge():
    operators = ('+', '*', '-',)
    operands = (random.randint(1, 10), random.randint(1, 10))
    operator = random.choice(operators)
    if operands[0] < operands[1] and '-' == operator:
        operands = (operands[1], operands[0])
    challenge = '%d%s%d' % (operands[0], operator, operands[1])
    return '{}='.format(
        challenge.replace('*', api_settings.CAPTCHA_MATH_CHALLENGE_OPERATOR)
    ), eval(challenge)

