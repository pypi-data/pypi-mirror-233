from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name='geodata-preprocess-IIITB-SCL',
    version='0.1.1',
    author='IIITB-SCL',
    description='Dealing with Geopspatial Data, faster computation of ndvi indices using dask',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'rasterio',
        'dask',
        'dask.distributed',
        'matplotlib',
        'pandas',
        'scikit-learn',
    ],
)