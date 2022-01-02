import pathlib

from setuptools import setup

from crossy import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="crossy",
    version=__version__,
    description="mRNA stability analysis",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/realpython/reader",
    author="Matthew Theisen",
    author_email="mtheisen@ucla.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["crossy"],
    include_package_data=True,
    install_requires=["pandas"],
    extras_require={"dev": ["pylint", "autopep8", "isort", "black"]},
    entry_points={"console_scripts": ["realpython=reader.__main__:main"]},
)
