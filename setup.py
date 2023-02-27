from setuptools import setup, find_packages

setup(
    name='easy_alias',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'pp=scripts.main:cli',
            'ppe=scripts.main:pae'
        ],
    },
)
