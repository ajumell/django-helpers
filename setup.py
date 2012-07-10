__author__ = 'ajumell'
from distutils.core import setup


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
    packages=['django_helpers'],
    install_requires=[
        "Django >= 1.4"
    ]
)
