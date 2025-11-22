"""
Setup script for chatapp client.
Installs the terminal chat app as a console command.
"""
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="chatapp",
    version="1.0.0",
    description="Secure ephemeral terminal chat application",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "chatapp=main:run",
        ],
    },
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Chat",
    ],
)
