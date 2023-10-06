
from setuptools import setup, find_packages

setup(
    name="kluffpythonsdk",
    version="0.0.0",
    packages=find_packages(where="./proto_svcs"),
    install_requires=[],
    python_requires='>=3.10',
    description="a library representing multiple apps of frappe",
    author="kluff",
)