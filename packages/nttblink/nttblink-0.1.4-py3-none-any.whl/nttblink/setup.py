from setuptools import setup, find_packages

setup(
    name='nttblink',
    version='0.1.2',
    packages=find_packages(),
    author='Austin Arlint',
    author_email='austin.arlint@global.ntt',
    description='A utility package for fetching secrets and documents from NTT Blink',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NTT-AM-DDD/python-nttblink',
    install_requires=['requests','python-dotenv']
)