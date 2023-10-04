# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

name = "onepi"
version = "1.0.2"
description = "Python library to interface with BotnRoll One A"
url = "https://github.com/ninopereira/bnronepi/tree/main/onepi"
author = "Nino Pereira"
author_email = "ninopereira.pt@gmail.com"
license = "MIT"
packages = find_packages()
py_modules=['one']
data_files=[
    ('config', ['utils/config.json']),
    ('requirements', ['requirements.txt']),
    ('test_cfg', ['tests/test_cfg.json']),
    ('config_line_follow', ['examples/line_sensor/config_line_follow.json']),
    ('config_line_follow_pid', ['examples/line_sensor/config_line_follow_pid.json']),
    ('config_line_follow_cosine', ['examples/line_sensor/config_line_follow_cosine.json'])
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

# Package dependencies
install_requires = ["spidev"]

setup(
    name=name,
    version=version,
    description=description,
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=install_requires,
)
