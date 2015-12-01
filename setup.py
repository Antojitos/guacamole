from setuptools import setup
from setuptools.command.test import test

with open('README.md') as file:
    long_description = file.read()


setup(
    name="guacamole-files",
    version="0.1.0",
    author="Antonin Messinger",
    author_email="antonin.messinger@gmail.com",
    description=" Upload any file, get a URL back",
    long_description=long_description,
    license="MIT License",
    url="https://github.com/Antojitos/guacamole",
    download_url="https://github.com/Antojitos/guacamole/archive/0.1.0.tar.gz",
    keywords=["guacamole", "url", "files"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ],

    packages=['guacamole'],
    install_requires=[
        'Flask==0.10.1',
        'Flask-PyMongo==0.4.0',
    ],

    test_suite='tests.main'
)
