from setuptools import setup, find_packages

setup(
    name='math_tool',
    version='1.0.0',
    author='Tom Alex',
    description='A collection of mathematical utility functions',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
    ],
)