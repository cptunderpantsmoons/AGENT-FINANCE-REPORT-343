#!/usr/bin/env python3
"""
Setup configuration for AASB Financial Statement Generator
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="aasb-financial-statement-generator",
    version="1.0.0",
    author="AASB Financial Statement Generator Team",
    author_email="support@example.com",
    description="Generate AASB-compliant financial statements for non-reporting entities",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/aasb-financial-statement-generator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "aasb-generator=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
