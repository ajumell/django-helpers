#! /usr/bin/python
__author__ = 'ajumell'
import os
from setuptools import setup, find_packages

PACKAGE_NAME = "django_helpers"
CUR_DIR = os.path.dirname(__file__)
CODE_DIR = os.path.join(CUR_DIR, PACKAGE_NAME)
EXCLUDED_DIRECTORIES = ["templates", "static", "tests"]
ADDITIONAL_DIRECTORIES = ["templates", "static"]
PACKAGES = find_packages(exclude=['django_helpers.tests', 'django_helpers.tests.*'])
PACKAGE_DATA = []

'''
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
setup(name = "mnemosyne",
      author = "Sune Kirkeby",
      url = "http://ibofobi.dk/stuff/mnemosyne/",
      version = '0.1',
      packages = ['ibofobi', 'ibofobi.apps', 'ibofobi.apps.mnemosyne',
                  'ibofobi.apps.mnemosyne.models',
                  'ibofobi.apps.mnemosyne.views',
                  'ibofobi.apps.mnemosyne.urls'],
      package_dir = {'': 'src'},
      package_data = {'ibofobi.apps.mnemosyne': ['templates/mnemosyne/*.html',
                                                 'static/*',],},
      # distutils complain about these, anyone know an easy way to silence it?
      namespace_packages = ['ibofobi.apps'],
      zip_safe = True,
)

setup(name='django-extrawidgets',
      version='1',
      description='A project exploring the client-side of Django website development',
      long_description=long_description,
      author='Russell Keith-Magee',
      author_email='russell@keith-magee.com',
      url='http://www.bitbucket.org/freakboy3742/django-rays/wiki/',
      packages=['django_extrawidgets'],
      classifiers=['Development Status :: 1 - Planning',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities'],
      zip_safe=False,
      tests_require=[],
      include_package_data=True #To include static files in app
      )
'''

for d in ADDITIONAL_DIRECTORIES:
    d = os.path.join(PACKAGE_NAME, d)
    for directory in os.walk(d):
        path = directory[0][len(PACKAGE_NAME) + 1:] + '/*.*'
        PACKAGE_DATA.append(path)

print '\n' * 2
for x in PACKAGE_DATA: print x
print '\n' * 2
for PACKAGE in PACKAGES: print PACKAGE
print '\n' * 2
print {PACKAGE_NAME: PACKAGE_DATA}
print '\n' * 2

# PACKAGE_DATA = ['templates/*', 'static/*']

setup(
    name='django-helpers',
    version='0.0.1',
    long_description='',
    description='Django Helpers and form addons.',
    author='Muhammed K K',
    author_email='ajumell@gmail.com',
    url="http://www.xeoscript.com/",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django'
    ],
    platforms=["any"],
    license="Freely Distributable",

    # package_data={PACKAGE_NAME: PACKAGE_DATA},
    packages=PACKAGES,

    install_requires=[
        "Django >= 1.4"
    ],
    zip_safe=False,
    include_package_data=False
)
