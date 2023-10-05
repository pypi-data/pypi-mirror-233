from setuptools import setup, find_packages

setup(
    name="StreamLoom",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author="Sandeep S Kumar",
    author_email="sanygeek@gmail.com",
    description="A modular and extensible Python framework for building, managing, and executing pipelines.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/creativesands/streamloom",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
