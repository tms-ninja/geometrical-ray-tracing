# Compile using python setup.py build_ext --inplace
import numpy as np
from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("tracing.pyx", compiler_directives={'language_level': 3}),
      include_dirs=[np.get_include()])

