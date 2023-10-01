from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lockfile-parser",  # Replace with your desired package name
    version="0.2.0",
    author="Nikhil",
    author_email="nm2868@columbia.edu",
    description="A mininal lockfile parser in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nikhilmitrax/lockfile-parser-py",  # Replace with your repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "toml>=0.10.2",  # Adjust the version as needed
    ],
)
