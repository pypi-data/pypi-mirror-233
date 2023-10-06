import setuptools
from hyc import version

setuptools.setup(
    name="hyc",
    packages=setuptools.find_packages(),
    version=version,
    url="https://github.com/offical-HYC/hyc",
    license="MIT",
    description="HYC means HELP YOU CALCULATE.It has many functions to help you calculate quickly and easily.",
    # long_description=open("README.md").read(),
    author="Zou",
    author_email="HUWA625@outlook.com",
    keywords=["calculate", "maths"],
    classifiers=[
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Natural Language :: Chinese (Simplified)"
    ],
)
