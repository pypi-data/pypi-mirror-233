from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

testaaa = find_packages()

setup(
    name='steam-models',
    version="2023.10.0",
    author="STEAM Team",
    author_email="steam-team@cern.ch",
    description="Models for APIs for STEAM tools.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://gitlab.cern.ch/steam/steam_models",
    keywords=['STEAM', 'simulation', 'models', 'CERN'],
    install_requires=required,
    python_requires='>=3.8',
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8"
        ],
)
