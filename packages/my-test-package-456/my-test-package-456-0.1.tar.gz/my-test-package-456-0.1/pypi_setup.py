from setuptools import find_packages, setup

with open("PYPI_README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="my-test-package-456",
    version="0.1",
    packages=find_packages(include=["test_package_kNzQoY"]),
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
