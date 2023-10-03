from setuptools import setup, find_packages

NAME = "pyfmg-ng"
VERSION = '0.0.1'

REQUIRES = (["requests", "logging", "urllib3"])

setup(
    name=NAME,
    version=VERSION,
    description="Python Fortimanager SDK NG",
    url="https://github.com/pertoft/pyfmg-ng",
    author="Per Abildgaard Toft",
    author_email="p@t1.dk",
    packages=find_packages(include=["pyfmg-ng"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=REQUIRES,
    license="GPL",
    keywords=["FortiManager", "FortiNet", "FortiGate"],
)
