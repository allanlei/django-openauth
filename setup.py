from distutils.core import setup
from setuptools import find_packages
import os
import sys

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def find_packages_in(where, **kwargs):
    return [where] + ['%s.%s' % (where, package) for package in find_packages(where=where, **kwargs)]

setup(
    name = 'django-openauth',
    version = '0.3.3',
    author = 'Allan Lei',
    author_email = 'allanlei@helveticode.com',
    description = ('OpenID/OAuth for Django'),
    license = 'New BSD',
    keywords = 'openid oauth django',
    url = 'https://github.com/allanlei/django-openauth',
    packages=find_packages_in('openauth'),
    long_description=read('README.md'),
    install_requires=[
        'python-openid==2.2.5',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
