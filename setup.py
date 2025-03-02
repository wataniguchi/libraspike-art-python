from setuptools import setup

setup(
    cffi_modules=["libraspike_art_python/ffi_build.py:ffibuilder"]
)
