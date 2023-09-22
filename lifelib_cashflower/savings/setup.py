from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy as np

# Define the extension module
extensions = [
    Extension("discount", ["discount.pyx"],
              include_dirs=[np.get_include()]),  # Add the NumPy include directory
]

setup(
    ext_modules=cythonize(extensions),
)
