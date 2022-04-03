# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = '1.0.0'


ext_modules = [
    Pybind11Extension(
        'mesh2sdf',
        ['csrc/pybind.cpp', 'csrc/makelevelset3.cpp'],
        include_dirs=['csrc'],
        define_macros=[('VERSION_INFO', __version__)],),
]

setup(
    name='mesh2sdf',
    version=__version__,
    author='Peng-Shuai Wang',
    author_email='wangps@hotmail.com',
    url='https://github.com/wang-ps/mesh2sdf',
    description='Compute the signed distance field from an input mesh',
    long_description='',
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    zip_safe=False,
    python_requires='>=3.6',
)
