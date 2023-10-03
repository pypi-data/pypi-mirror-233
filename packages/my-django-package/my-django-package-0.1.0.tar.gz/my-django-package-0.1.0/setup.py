from setuptools import setup, find_packages

setup(
    name='my-django-package',
    version='0.1.0',
    author= 'Neha Yargal',
    author_email='nehayargal@fortna.com',
    packages=find_packages(),
    install_requires=[
        'Django',
        # Add any other dependencies here
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
