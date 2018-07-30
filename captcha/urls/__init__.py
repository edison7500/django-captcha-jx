from django.conf.urls import url
from captcha.views import CaptchaView


urlpatterns = [
    url(r'^$', CaptchaView.as_view(), name='captcha-image'),
]