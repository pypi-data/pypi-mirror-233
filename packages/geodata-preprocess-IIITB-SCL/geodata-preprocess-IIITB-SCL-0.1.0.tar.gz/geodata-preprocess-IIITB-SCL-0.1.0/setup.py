from setuptools import setup, find_packages

setup(
    name='geodata-preprocess-IIITB-SCL',
    version='0.1.0',
    author='IIITB-SCL',
    description='Dealing with Geopspatial Data, faster computation of ndvi indices using dask',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'rasterio',
        'dask',
        'matplotlib',
        'pandas',
        'scikit-learn',
    ],
)