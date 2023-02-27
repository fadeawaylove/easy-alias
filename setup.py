import os
from setuptools import setup, find_packages

long_description = open(os.path.join(os.path.dirname(__file__), "README.md"), "r", encoding="utf-8").read()

setup(
    name='easy_alias',
    version='0.1',
    author="daigua",
    author_email="1032939141@qq.com",
    description="A simple and easy command alias tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fadeawaylove/easy_alias",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Click'],
    entry_points={
        'console_scripts': [
            'pp=scripts.main:cli',
            'ppe=scripts.main:pae'
        ],
    },
    python_requires='>=3.6'
)