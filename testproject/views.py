import base64
import uuid

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import caches
from captcha.conf.settings import api_settings
from captcha import helpers
from captcha.challenge import Captcha

cache = caches[api_settings.CAPTCHA_CACHE]


class CaptchaAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def _generate_captcha(self, requests):
        key = str(uuid.uuid4())
        value = helpers.random_char_challenge(api_settings.CAPTCHA_LENGTH)
        cache_key = helpers.get_cache_key(key)
        cache.set(cache_key, value, api_settings.CAPTCHA_TIMEOUT)

        image_bytes = Captcha(word=value).generate_image()
        image_b64 = base64.b64encode(image_bytes)
        data = {
            api_settings.CAPTCHA_KEY: key,
            api_settings.CAPTCHA_IMAGE: image_b64,
            'image_type': 'image/png',
            'image_decode': 'base64'
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self._generate_captcha(request)

    def get(self, request):
        return self._generate_captcha(request)
