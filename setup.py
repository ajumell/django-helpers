#! /usr/bin/python

__author__ = 'ajumell'

from time import time
from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES
from distutils.command.install_data import install_data

import os
import sys


class osx_install_data(install_data):
    # On MacOS, the platform-specific lib dir is /System/Library/Framework/Python/.../
    # which is wrong. Python 2.5 supplied with MacOS 10.5 has an Apple-specific fix
    # for this in distutils.command.install_data#306. It fixes install_lib but not
    # install_data, which is why we roll our own install_data class.

    def finalize_options(self):
        # By the time finalize_options is called, install.install_lib is set to the
        # fixed directory, so we set the installdir to install_lib. The
        # install_data class uses ('install_data', 'install_dir') instead.
        self.set_undefined_options('install', ('install_lib', 'install_dir'))
        install_data.finalize_options(self)

if sys.platform == "darwin":
    cmdclasses = {'install_data': osx_install_data}
else:
    cmdclasses = {'install_data': install_data}

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell distutils not to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
project_dir = 'django_helpers'

for dirpath, dirnames, filenames in os.walk(project_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

# Small hack for working with bdist_wininst.
# See http://mail.python.org/pipermail/distutils-sig/2004-August/004134.html
if len(sys.argv) > 1 and sys.argv[1] == 'bdist_wininst':
    for file_info in data_files:
        file_info[0] = '\\PURELIB\\%s' % file_info[0]

# Dynamically calculate the version based on django.VERSION.
version = __import__('django').get_version()

setup(
    name='django-helpers',
    version='0.0.1-alpha-' + str(time()),
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

    packages=packages,
    cmdclass=cmdclasses,
    data_files=data_files,

    install_requires=[
        "Django >= 1.4"
    ],

    zip_safe=False
)
x = """

setup(
    name = "Django",
    version = version,
    url = 'http://www.djangoproject.com/',
    author = 'Django Software Foundation',
    author_email = 'foundation@djangoproject.com',
    description = 'A high-level Python Web framework that encourages rapid development and clean, pragmatic design.',
    download_url = 'https://www.djangoproject.com/m/releases/1.4/Django-1.4.tar.gz',
    packages = packages,
    cmdclass = cmdclasses,
    data_files = data_files,
    scripts = ['django/bin/django-admin.py'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )










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
"""