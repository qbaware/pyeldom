import os
from setuptools import setup, find_packages

# Check if a version argument is passed via environment variable.
if "PACKAGE_VERSION" in os.environ:
    version = os.environ["PACKAGE_VERSION"]
else:
    raise Exception("Version is required to be passed as an environment variable.")

# Setup the package.
setup(
    name="pyeldom",
    version=version,
    description="A Python client for the Eldom API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Daniel Gospodinow",
    author_email="danielgospodinow@gmail.com",
    url="https://github.com/qbaware/pyeldom",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
