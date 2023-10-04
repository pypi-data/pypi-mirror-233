from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name='HighGeoX',
    version='0.1.1',
    author='Deeksha Aggarwal',
    description='provides utilities to deal with large geospatial Datasets and provides functions for Fast computation of NDVI and MNDVI indces,',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'rasterio',
        'dask',
        'distributed',
        'matplotlib',
        'pandas',
        'scikit-learn',
    ],
)