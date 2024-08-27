from setuptools import setup, find_packages

setup(
    name="pyeldom",
    version="0.0.5",
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
