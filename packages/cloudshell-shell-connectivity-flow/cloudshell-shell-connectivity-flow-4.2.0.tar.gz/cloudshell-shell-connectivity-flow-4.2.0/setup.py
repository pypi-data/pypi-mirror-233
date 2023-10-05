import os

from setuptools import find_packages, setup

with open(os.path.join("version.txt")) as version_file:
    version_from_file = version_file.read().strip()

with open("requirements.txt") as f_required:
    required = f_required.read().splitlines()

with open("test_requirements.txt") as f_tests:
    required_for_tests = f_tests.read().splitlines()

setup(
    name="cloudshell-shell-connectivity-flow",
    url="https://www.quali.com/",
    author="QualiSystems",
    author_email="info@qualisystems.com",
    packages=find_packages(),
    install_requires=required,
    tests_require=required_for_tests,
    python_requires="~=3.9",
    version=version_from_file,
    description="QualiSystems Shells Connectivity Flow Package",
    long_description="QualiSystems Shells Connectivity Flow Package",
    long_description_content_type="text/x-rst",
    include_package_data=True,
)
