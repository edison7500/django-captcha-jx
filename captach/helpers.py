import random
import os
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from math import ceil
from io import BytesIO

current_path = os.path.normpath(os.path.dirname(__file__))

words = "ABCEDFGHIJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"