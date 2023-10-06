from setuptools import find_packages, setup


def find_required():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="vedro-screenshot-matcher",
    version="0.1.0",
    description="Playwright plugin for matching screenshots with Vedro Testing Framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="MashaJing",
    author_email="mdzekh23032000a@gmail.com",
    python_requires=">=3.9",
    url="https://github.com/MashaJing/vedro-screenshot-matcher",
    project_urls={
        "GitHub": "https://github.com/MashaJing/vedro-screenshot-matcher",
    },
    license="Apache-2.0",
    packages=find_packages(exclude=("tests",)),
    install_requires=find_required(),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
