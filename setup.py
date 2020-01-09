#!/usr/bin/env python3

from setuptools import setup
import docker_sigprofiler


setup (
    name = 'docker-sigprofiler', 
    description = 'Code for creating SigProfiler docker containers', 
    author = 'Jingwei Wang', 
    url = 'https://github.com/cancerit/docker-sigprofiler', 
    author_email = 'cgphelp@sanger.ac.uk', 
    license='agpl-3.0',
    version = docker_sigprofiler.version, 
    python_requires = '>= 3.6', 
    packages = ['docker_sigprofiler'], 
    install_requires = [
        'Sigproextractor==0.0.5.77',
        'SigprofilerPlotting==1.0.10',
        'SigprofilerMatrixGenerator==1.0.21',
        'xlrd'
    ], 
    entry_points={
        'console_scripts': [
            'docker-sigprofiler=docker_sigprofiler.command_line:main',
        ],
    },
)
