from setuptools import setup, find_packages

setup(
    name='gmail_send',
    version='0.1',
    description='Una librería para enviar correos electrónicos usando Gmail',
    author='aslskks',
    author_email='davikenat@gmail.com',
    packages=find_packages(),
    install_requires=[
        "smtplib",
        "email"
    ],
)