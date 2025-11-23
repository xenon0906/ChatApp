"""
ChatApp - Secure Ephemeral Messaging
Setup script for pip installation
"""
from setuptools import setup, find_packages
import os

# Read README
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "Secure ephemeral messaging with end-to-end encryption"

setup(
    name="chatapp-cli",
    version="1.0.0",
    author="ChatApp Team",
    author_email="contact@chatapp.example.com",
    description="Secure ephemeral messaging with end-to-end encryption",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xenon0906/ChatApp",
    packages=["chatapp_package"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Chat",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "chatapp=chatapp_package.main:main",
        ],
    },
)
