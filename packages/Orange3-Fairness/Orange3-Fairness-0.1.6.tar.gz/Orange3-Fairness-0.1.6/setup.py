from setuptools import setup, find_packages
from os import path

VERSION = "0.1.6"

try:
    LONG_DESCRIPTION = open(
        path.join(path.dirname(__file__), "README.pypi"), "r", encoding="utf-8"
    ).read()
except FileNotFoundError:
    LONG_DESCRIPTION = ""

setup(
    name="Orange3-Fairness",
    version=VERSION,
    author="Bioinformatics Laboratory, FRI UL",
    author_email="info@biolab.si",
    maintainer="Zan Mervic",
    url="https://github.com/biolab/orange3-fairness",
    description="Orange3 add-on for fairness-aware machine learning.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license="GPL3+",
    keywords=(
        "orange3 add-on",
        "orange3 fairness",
    ),

    packages=find_packages(),
    package_data={
        "orangecontrib.fairness.widgets": ["icons/*"],
        },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        ],
    entry_points={
        "orange3.addon": ("Orange3-Fairness = orangecontrib.fairness",),
        "orange.widgets": ("Fairness = orangecontrib.fairness.widgets",),
        },
    install_requires=[
        "Orange3",
        "aif360==0.5.0",
        "numpy~=1.23.0"
    ],
    extras_require={
        "doc": [
            "sphinx",
            "sphinx_rtd_theme",
            "recommonmark",
        ]
    },
)