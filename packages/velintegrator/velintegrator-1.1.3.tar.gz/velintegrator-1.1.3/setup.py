from setuptools import setup, find_packages

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='velintegrator',
    version='1.1.3',
    description='Veli Third Party Integrator',
    author='Dachi',
    author_email='dvadachkoria@veli.store',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages()
)
