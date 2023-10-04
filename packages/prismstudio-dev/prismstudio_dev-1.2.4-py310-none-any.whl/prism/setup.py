import os
from glob import glob
from dotenv import dotenv_values
from setuptools import setup, find_packages


env = os.environ['ENV_STATE']
name = "prismstudio"
version = dotenv_values("./_common/.env").get("VERSION", "")

datafiles = [("prism/_common", ["prism/_common/.env"])]
if env == 'dev' or env == 'stg' or env == 'demo':
    name = name + '-' + env

setup(
    name=name,
    version=version,
    description="Python Extension for PrismStudio",
    author="Prism39",
    author_email="jmp@prism39.com",
    url="https://www.prism39.com",
    packages=find_packages(),
    license="Prism39 End User License",
    python_requires=">=3.8",
    # data_files=datafiles,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        "pandas==2.0.3",
        "pyarrow==12.0.0",
        "tqdm==4.64.0",
        "orjson==3.9.3",
        "requests==2.26.0",
        "pydantic[dotenv]==1.10.2",
        "pyzmq==24.0.1",
        "python-dotenv==1.0.0",
        "numpy==1.26.0"
    ],
    include_package_data=True
)