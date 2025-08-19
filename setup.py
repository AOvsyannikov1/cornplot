from setuptools import setup, find_packages, Extension
from os.path import join, dirname


c_files = ['cornplot/array_utils.c']
c_extension_name = "cornplot.array_utils"
# Создание C-расширения
extension = Extension(
    c_extension_name,
    c_files,
    include_dirs=[],  # добавьте дополнительные include директории если нужно
    libraries=[],      # добавьте библиотеки если нужно
    library_dirs=[]    # добавьте пути к библиотекам если нужно
)

setup(
    name="cornplot",
    version="3.0",
    packages=find_packages(include=['cornplot', 'cornplot.*', '*.pyd']),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    ext_modules=[extension],
    package_data={
        "cornplot": [
            "images/*.png",
        ]
    },
    include_package_data=True,
    entry_points={
        'pyinstaller40': [
            'hook-dirs = cornplot:_get_hook_dirs',
        ],
    },
    install_requires=[
        "scipy>=1.16.1",
        "PyQt6>=6.9.0"
    ],
    author="Ovsiannikov Andrey",
    author_email="andsup108@gmail.com"
)
