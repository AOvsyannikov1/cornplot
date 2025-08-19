from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name="cornplot",
    version="3.0",
    packages=find_packages(include=['cornplot', 'cornplot.*', '*.pyd']),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    package_data={
        "cornplot": [
            "images/*.png",
            "*.pyd"
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
