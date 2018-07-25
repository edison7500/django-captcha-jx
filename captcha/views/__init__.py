import uuid

from captcha import helpers
from django.views import View
from django.http import HttpResponse
from django.core.cache import caches
from captcha.conf.settings import api_settings
from captcha import helpers
from captcha.challenge import Captcha

cache = caches[api_settings.CAPTCHA_CACHE]


class CaptchaView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        key = str(uuid.uuid4())
        value = helpers.random_char_challenge(api_settings.CAPTCHA_LENGTH)
        cache_key = helpers.get_cache_key(key)
        cache.set(cache_key, value, api_settings.CAPTCHA_TIMEOUT)
        image_bytes = Captcha(word=value).generate_image()

        return HttpResponse(content=image_bytes, content_type='image/png')
