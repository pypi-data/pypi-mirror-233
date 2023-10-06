from setuptools import setup
import setuptools


setup(
    name="NRandom",
    version="1.0",
    description="This module also help in figure out  the most similar text in the given dataset with user given input.....",
    author="Somnath Dash",
    packages=setuptools.find_packages(),
    keywords=["Random","Not Random"],
    license="./LICENSE.txt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    requires=[
        "sklearn",
        "numpy"
        ],
    install_requires=[
        "scikit-learn",
        "numpy"
        ],
        
)