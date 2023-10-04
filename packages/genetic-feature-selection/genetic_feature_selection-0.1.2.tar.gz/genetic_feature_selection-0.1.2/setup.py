from setuptools import find_packages
from setuptools import setup
from __version__ import __version__


def read(file_name):
    with open(file_name, "r") as f:
        txt = f.read()
    return txt


setup(
    name='genetic_feature_selection',
    description='Program for selecting the n best features for your machine learning model.',
    long_description=read("README.rst"),
    author='Magnus P. Nytun',
    author_email='magnus.nytun@sb1ostlandet.no',
    version=__version__,
    packages= find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn"
    ]
)
