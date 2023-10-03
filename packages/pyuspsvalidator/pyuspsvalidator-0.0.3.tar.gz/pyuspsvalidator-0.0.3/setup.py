from setuptools import setup

with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pyuspsvalidator",
    version="0.0.3",
    packages=['pyuspsvalidator'],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    install_requires=[
        "requests>=2.31.0",
    ],
)
