#!/usr/bin/env python
import os
import re

from setuptools import setup, find_packages


version = re.compile(r'VERSION\s*=\s*\((.*?)\)')


def get_package_version():
    "returns package version without importing it"
    base = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base, "tracker/__init__.py")) as initf:
        for line in initf:
            m = version.match(line.strip())
            if not m:
                continue
            return ".".join(m.groups()[0].split(", "))


classes = """
    Development Status :: 3 - Alpha
    Intended Audience :: Developers
    License :: OSI Approved :: BSD License
    Topic :: System :: Monitoring
    Topic :: System :: Distributed Computing
    Programming Language :: Python
    Programming Language :: Python :: 2
    Programming Language :: Python :: 2.6
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: Implementation :: CPython
    Operating System :: OS Independent

"""
classifiers = [s.strip() for s in classes.split('\n') if s]


setup(
    name='celery-tracker',
    version=get_package_version(),
    description='Receive/Sending event tracking data for the Celery',
    long_description=open('README.rst').read(),
    keywords=['django', 'celery', 'tracking', 'agent', 'metrics'],
    author='Tatsuo Ikeda',
    author_email='jp.ne.co.jp at gmail.com',
    url='https://github.com/ikeikeikeike/celery-tracker',
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'celery',
        'celerymon',
        'simplejson',
        'tornado',
        'fluent-logger',
        'zbxsend'
    ],
    package_data={'tracker': ['templates/*', 'static/**/*']},
    entry_points={
        "console_scripts": [
            "tracker = tracker.bin.tracker:main",
        ],
        "celery.commands": [
            "tracker = tracker.bin.tracker:TrackerDelegate",
        ],
    }
)
