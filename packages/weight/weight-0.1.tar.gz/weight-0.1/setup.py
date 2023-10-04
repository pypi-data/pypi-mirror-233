from setuptools import setup

setup(
    name='weight',
    version='0.1',
    packages=['weight'],
    install_requires=[
        'click',
        'matplotlib',
        "configparser"
    ],
    entry_points='''
        [console_scripts]
        weight=weight.cli:main
    ''',
)