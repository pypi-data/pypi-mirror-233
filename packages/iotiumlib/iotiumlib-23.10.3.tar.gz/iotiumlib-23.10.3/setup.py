import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iotiumlib",
    version="23.10.03",
    author="Rashtrapathy C",
    author_email="rashtrapathy.chandrasekar@view.com",
    description="ioTium API library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://view.com",
    packages=setuptools.find_packages(),
    license="Copyright 2023 View, Inc. | All Rights Reserved.",
    classifiers=(
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'requests',
        'urllib3'
    ]
)
