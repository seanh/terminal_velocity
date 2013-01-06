from setuptools import setup

setup(
    name="terminal_velocity",
    version="0.1a7",
    author="Sean Hammond",
    packages=["terminal_velocity"],
    scripts=["bin/terminal_velocity"],
    url="http://seanh.github.com/terminal_velocity/",
    license="GNU General Public License, Version 3",
    description="A fast note-taking app for the UNIX terminal",
    long_description=open("README.rst").read(),
    install_requires=[
        "urwid==1.1.1",
        "chardet==2.1.1",
        ]
)
