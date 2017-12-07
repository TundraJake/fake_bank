from setuptools import setup

setup(
    name='muh_bank',
    packages=['muh_bank'],
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy',
    ],
)