#!/usr/bin/env python3

from setuptools import setup

setup (
    name = 'docker-sigprofiler', 
    description = 'a implementation for sigprofiler docker CI', 
    author = 'Jingwei Wang', 
    url = 'www.example.com', 
    author_email = 'jw32@sanger.ac.uk', 
    version = '0.1.0', 
    python_requires = '>= 3.6', 
    packages = ['docker_sigprofiler'], 
    install_requires = [
        ''
    ], 
    entry_points={
        'console_scripts': [
            'docker-sigprofiler=docker_sigprofiler.command_line:main',
        ],
    },
)
