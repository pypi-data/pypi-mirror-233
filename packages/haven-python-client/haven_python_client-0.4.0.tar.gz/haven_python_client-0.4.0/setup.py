from setuptools import setup, find_packages

setup(
    name="haven_python_client",
    version="0.4.0",
    author="Haven",
    author_email="hello@haven.run",
    description="Python client for Haven endpoints",
    packages=find_packages(),
    install_requires=[
        "requests",
        "munch"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)