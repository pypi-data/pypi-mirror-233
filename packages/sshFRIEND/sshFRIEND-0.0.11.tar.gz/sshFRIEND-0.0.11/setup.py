import os
from setuptools import setup

def read(fname):
    with open("README.md") as f:
        return f.read()

setup(
    name = "sshFRIEND",
    version = "0.0.11",
    author = "David Johnnes",
    author_email = "david.johnnes@gmail.com",
    description = ("A generic and platform agnostic SSH module to access and send commands to remote devices that support OpenSSH"),
    license = "BSD",
    keywords = "ssh access, ssh remote command execution",
    url = "",
    packages=['sshFRIEND'],
    long_description=read('README.md'),
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
)