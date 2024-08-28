import sys
from setuptools import setup, find_packages

# Check if a version argument is passed.
if len(sys.argv) > 1 and sys.argv[1].startswith("--version="):
    version = sys.argv[1].split("=")[1]
    sys.argv = [sys.argv[0]] + sys.argv[2:]
else:
    raise Exception("Version argument is required")

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
