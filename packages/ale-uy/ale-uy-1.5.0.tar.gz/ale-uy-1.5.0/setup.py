from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='ale-uy',
    version='1.5.0',
    description='Tool to perform data cleaning, modeling and visualization in a simple way.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='ale-uy',
    author_web='https://ale-uy.github.io/',
    url='https://github.com/ale-uy/DataScience',
    packages=find_packages(),
    install_requires=requirements,
)
