from setuptools import setup, find_packages

setup(
    name="wivigraph",
    version="1.1.1",
    packages=find_packages(),
    install_requires=["graphql-core","requests"],
)