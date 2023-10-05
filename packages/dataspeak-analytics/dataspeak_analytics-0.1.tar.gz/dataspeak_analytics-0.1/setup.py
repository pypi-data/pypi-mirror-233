from setuptools import setup, find_packages

setup(
    name="dataspeak_analytics",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'mixpanel',
        'pymongo',
        'python-dotenv'
    ],
    author="Alejandro Radisic",
    author_email="aleradisic@gmail.com",
    description="A library for analytics using Mixpanel and MongoDB",
    long_description=open('./README.md').read(),
    long_description_content_type='text/markdown',
)
