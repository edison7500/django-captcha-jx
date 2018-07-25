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


def random_color():
    return (
        random.randrange(
            120, 255), random.randrange(
            120, 255), random.randrange(
            120, 255), random.randrange(
            230, 255)
    )


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


def filter_smooth(image, filter_code):
    return image.filter(filter_code)


def noise_dots(draw, image, fill):
    size = image.size
    for p in range(int(size[0] * size[1] * 0.1)):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        draw.point((x, y), fill=fill)
    return draw


def noise_arcs(draw, image):
    size = image.size
    for p in range(int(size[0] * size[1] * 0.1)):
        draw.point((random.randint(0, size[0]), random.randint(0, size[1])), fill=random_color())
    return draw
