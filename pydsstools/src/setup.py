from setuptools import Command, Extension, setup, find_packages
from setuptools.command.build_ext import build_ext
import os
from os.path import join 
import sys
import platform
from subprocess import call
import shutil
import numpy

try:
    from Cython.Build import cythonize
    _CYTHON_INSTALLED = True
except:
    _CYTHON_INSTALLED = False

setup_dir = os.path.abspath(os.path.dirname(__file__))
print('setup directory: %r'%setup_dir)

arch_x64 = False
if sys.maxsize > 2**32:
    arch_x64 = True

if not arch_x64:
    raise Exception('Only the 64-bit Python is supported')

def is_platform_windows():
    return sys.platform == "win32" or sys.platform == "cygwin"

def is_platform_mac():
    return sys.platform == "darwin"    

def is_platform_linux():
    return sys.platform == "linux"


class BuildExt(build_ext):
    def build_grid_library(self):
        if is_platform_windows():
            print('Building external library: grid.lib')
            batch_file = join(setup_dir, r'external/gridv6/build.bat ')
            call(batch_file)
        else:
            print('Building external library: grid.a')
            make_dir = join(setup_dir, r'external/gridv6')
            batch_file = join(setup_dir, r'external/gridv6/build.sh')
            with open(batch_file, 'rb') as fid:
                script = fid.read()
            print('CWD: %s'%make_dir )
            call(script, shell=True, cwd=make_dir)

    def build_extensions(self):
        self.build_grid_library()
        super().build_extensions()


# Create compiler arguments
include_dirs = []
include_dirs.append(r'external/dss/headers')
include_dirs.append(r'external/gridv6/headers')
library_dirs = []

if is_platform_windows():
    # headers
    include_dirs.append(r'external/zlib')
    # lib dirs
    library_dirs.append(r'external/dss/win64')
    library_dirs.append(r'external/gridv6/build')
    library_dirs.append(r'external/zlib')
    # libs
    libraries = ['heclib_c', 'heclib_f', 'zlibstatic', 'grid']
    # extra compile args
    extra_compile_args = []
    extra_link_args = ['/NODEFAULTLIB:LIBCMT']

else:
    # lib dirs
    library_dirs.append(r'external/dss/linux64')
    library_dirs.append(r'external/gridv6/build')
    # libs
    libraries = [':heclib.a', ':grid.a','gfortran', 'pthread', 'm', 'quadmath', 'z', 'stdc++']
    # extra compile args
    extra_compile_args = []
    extra_link_args = []

include_dirs.append(numpy.get_include())

compiler_directives = {
    'embedsignature': True,
    'language_level': '3',
    'c_string_type': 'str',
    'c_string_encoding': 'ascii'
}

setup(
    name='heclib-c',
    version="2.4.1",
    ext_modules=[
        Extension(
            "pydsstools._lib.x64.core_heclib",
            sources =   [r'core_heclib.pyx'],
            include_dirs = include_dirs,
            library_dirs = library_dirs,
            libraries = libraries,
            define_macros = [],
            extra_compile_args = extra_compile_args,
            extra_link_args = extra_link_args,
        )
    ],

    build_ext={"build_ext": BuildExt},
)