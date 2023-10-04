from setuptools import setup, find_packages, Extension
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Define the extension module for your C++ code
schedulers_cpp_extension = Extension(
    'scheduling_utils.schedulers_cpp',  # Name of the Python module
    sources=['scheduling_utils/cpp_extensions/schedulers.cpp'],  # Path to C++ source file
    libraries=[],
    include_dirs=[],
)

setup(name='scheduling_utils',
      version='0.2.0',
      description='implementation of LR scheduling functions in c++, binded using ctypes',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/SerezD/scheduling_utils',
      author='DSerez',
      license='MIT',
      packages=['scheduling_utils'],
      ext_modules=[schedulers_cpp_extension],
      zip_safe=False,
      include_package_data=True)
