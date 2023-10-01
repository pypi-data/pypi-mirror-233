from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pypeepa",
    version="5.1",
    author="Ishfaq Ahmed",
    author_email="ishfaqahmed0837@gmail.com",
    description="Custom built utilities for general use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IshfaqAhmedProg/PyPeepa",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "alive-progress>=1.6.0",
        "pyfiglet>=0.8.post1",
        "psutil>=5.9.5",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
