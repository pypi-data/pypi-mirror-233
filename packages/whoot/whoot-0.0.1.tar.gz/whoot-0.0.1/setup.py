import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whoot",
    version="0.0.1",
    author="Katie Garwood",
    author_email="kgarwood@sdzwa.org",
    description="Tools for analyzing, capturing, and parsing audio data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/conservationtechlab/whoot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
