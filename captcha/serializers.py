from rest_framework import serializers
from django.utils.translation import ugettext as _
from django.core.cache import caches
from captcha.conf.settings import api_settings
from captcha import helpers


cache = caches[api_settings.CAPTCHA_CACHE]


class CaptchaSerializer(serializers.Serializer):
    captcha_key = serializers.CharField(max_length=64)
    captcha_value = serializers.CharField(min_length=4, trim_whitespace=True)

    def validate(self, data):
        super(CaptchaSerializer, self).validate(data)
        cache_key = helpers.get_cache_key(data['captcha_key'])

        if data['captcha_key'] in api_settings.MASTER_CAPTCHA:
            real_value = api_settings.MASTER_CAPTCHA[data['captcha_key']]
        else:
            real_value = cache.get(cache_key)

        if real_value is None:
            raise serializers.ValidationError(
                 _('Invalid or expired captcha key'))

        cache.delete(cache_key)
        if data['captcha_value'].upper() != real_value:
            raise serializers.ValidationError(_('Invalid captcha value'))
        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
