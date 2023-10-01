# setup.py

from setuptools import setup, find_packages

setup(
    name='createllm',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Khushal Jethava',
    description='Python package that let you create own transformers based models on your own data',
    url='https://github.com/khushaljethava/createllm',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent'
    ],
)
