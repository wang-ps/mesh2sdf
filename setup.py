from setuptools import setup
# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext

__version__ = '1.1.0'


with open("README.md", "r", encoding="utf-8") as fid:
  long_description = fid.read()

ext_modules = [
    Pybind11Extension(
        'mesh2sdf.core',
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
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['mesh2sdf'],
    package_dir={'mesh2sdf': 'mesh2sdf'},
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "trimesh",
        'scikit-image',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
