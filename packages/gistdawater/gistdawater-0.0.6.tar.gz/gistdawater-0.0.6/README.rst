
Lazyearth: Python earth science package

What is it?

Lazyearth is a Python package that offers ease and speed in analyzing geospatial data. Lazyearth was designed to support the functions of the Open Data Cube, which primarily aggregates aerial satellite imagery, but it can also operate on personal computers. The purpose of creating Lazyearth is for it to become a widely used tool in the field of geoscience.

- Website : https://lazyearth.org/
- PyPI : https://pypi.org/project/lazyearth/
- Mailing : Tun.k@ku.th
- Bug reports : https://github.com/Tun555/lazyearth/issues

Installation

If you want to work on a personal computer, you need to install the GDAL package first Open command prompt

conda install -c conda-forge gdal

However, if you want to work on Open Data Cube or Google Colab, you can get started immediately. The latest released version are available at the Python Package Index (PyPI)


pip install lazyearth


Main Features

Opening and Saving : It can open various types of images and save them easily in multiple formats after processing.
Image plotting : This feature supports the display of a diverse range of images for single or comparative purposes. It can accommodate various formats, such as 1 or 3-dimensional numpy arrays, as well as xarray.
Band combination : It can easily blend different color bands of satellite images
Remote Sensing Calculation: There are multiple calculation indices such as NDVI, EVI, BSI etc.
Water: This features water analysis, including water detection and water quality.



