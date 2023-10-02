from setuptools import find_packages, setup


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()



setup(
    name='fstlib',
    packages= find_packages(),
    version='1.0.1',
    description=''' A python library to read fst file. 
    Multithreaded serialization of compressed data frames using the 'fst' format. 
    The 'fst' format allows for full random access of stored data and a wide 
    range of compression settings using the LZ4 and ZSTD compressors.''',
    author='Vhiny-Guilley MOMBO',
    maintainer= "finres",
    install_requires=["rpy2", "pandas", "numpy"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    extras_require={
        "dev": ["pytest>=7.10", "twine>=4.0.2"]
        },
    python_requires = ">=3.10",
    long_description=long_description,
    long_description_content_type='text/markdown'
)