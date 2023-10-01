#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))

try:
    long = open("minecraft_launch\\README.md",encoding = "utf-8").read()
except:
    long = ""

setup(
    name='minecraft-launch-p',
    version='0.1.1',
    description='Python edition of MinecraftLaunch, a .Net Minecraft launcher core',
    author='JustRainy',
    author_email='1831719639@qq.com',
    url='https://github.com/Blessing-Studio/minecraft-launch-p',
    packages=find_packages(),
    install_requires=['aiofiles>=23.2.1', "urllib3>=2.0.4"],
    keywords='Minecraft launcher core',
    long_description=long,
    python_requires=">=3.11"
)