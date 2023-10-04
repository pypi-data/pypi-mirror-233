from setuptools import setup, find_packages, Extension
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Define the extension module for your C++ code
schedulers_cpp_extension = Extension(
    name='scheduling_utils.cpp_extensions.schedulers_cpp',
    sources=['scheduling_utils/cpp_extensions/schedulers.cpp']
)

setup(name='scheduling_utils',
      version='0.2.1',
      description='implementation of LR scheduling functions in c++, binded using ctypes',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/SerezD/scheduling_utils',
      author='DSerez',
      license='MIT',
      packages=find_packages(),
      ext_modules=[schedulers_cpp_extension],
      zip_safe=False,
      include_package_data=True)
