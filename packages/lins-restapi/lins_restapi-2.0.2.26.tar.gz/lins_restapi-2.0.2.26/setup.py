#!/usr/bin/env python

import os
import sys
from distutils.core import setup
from setuptools import find_packages


def get_version():
    return open('version.txt', 'r').read().strip()

setup(
    author='TI Sistemas',
    author_email='ti.sistemas@grupolinsferrao.com.br',    
    description='Classes e utilitarios para uso em apis rest com django.',        
    license='MIT',    
    name='lins_restapi',
    packages=find_packages(),    
    url='https://bitbucket.org/grupolinsferrao/pypck-lins-restapi/',
    version=get_version(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)