#!/usr/bin/env python

"""
setup.py file from SWIG example, adjusted
"""

from distutils.core import setup, Extension


BeamFormedFile_module = Extension('_BeamFormedFile',
                           sources=['BeamFormedFile.i', 'BeamFormedFile.cpp', 'HDF5File.cpp', 'HDF5Group.cpp'],
                           include_dirs=['/data/sys/opt/cep/hdf5/include'],
                           libraries=['hdf5'],
                           swig_opts=['-c++'],
                           language='c++',
                           )

setup (name = 'BeamFormedFile',
       version = '0.1',
       author      = "dr. Jan David Mol, ASTRON, the Netherlands",
       description = """Bindings of newDAL""",
       ext_modules = [BeamFormedFile_module],
       py_modules = ["BeamFormedFile"],
       )