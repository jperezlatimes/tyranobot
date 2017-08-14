#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="tyranobot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=(),
    author="James Perez",
    author_email="james.perez@tronc.com",
    description="Easily customizable Slackbot",
    long_description="An easily customizable Slackbot built on the SlackClient python library",
    url="https://github.com/jperezlatimes/tyranobot/",
    license="GNU GENERAL PUBLIC LICENSE",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat'
    ]
)
