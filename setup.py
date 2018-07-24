from setuptools import setup, find_packages
from captcha import __version__
# from setuptools.command.test import test as test_command
import sys

install_requires = [
    'Django >= 1.8',
    'Pillow >=2.2.2',
    'djangorestframework>=3.8',
]

setup(
    name='django-captcha-jx',
    version=__version__,
    author='jiaxin',
    author_email='edison7500@gmail.com',
    url="https://bitbucket.org/papaya2018/django-captcha-jx",
    license='MIT',
    packages=find_packages(exclude=['testproject', 'testproject.*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)
