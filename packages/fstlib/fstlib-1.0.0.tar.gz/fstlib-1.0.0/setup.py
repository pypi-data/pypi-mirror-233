from setuptools import find_packages, setup


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()



setup(
    name='fstlib',
    packages= find_packages(),
    version='1.0.0',
    description='R wrapper to handle fst files in pythoon',
    author='Vhiny-Guilley MOMBO',
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