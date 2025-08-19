# import tools to create the C extension

from distutils.core import setup, Extension

module_name = 'array_utils'
# the files your extension is comprised of
c_files = ['cornplot/array_utils.c']

extension = Extension(
    module_name,
    c_files
)

setup(
    name=module_name,
    version='1.0',
    description='The package description',
    author='Ovsyannikov Andrey',
    author_email='',
    url='',
    ext_modules=[extension]
)
