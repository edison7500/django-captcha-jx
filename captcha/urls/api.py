from django.conf.urls import url
from captcha.views.api import CaptchaAPIView


urlpatterns = [
    url(r'captcha/?$', CaptchaAPIView.as_view()),
]