from setuptools import setup, find_packages
setup(
    name="json-typed",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typing",
        "inspect",
        "collections",
        "json"
    ],
)
