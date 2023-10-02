from setuptools import find_packages, setup



from setuptools import setup
from setuptools.command.install import install
import subprocess
from setuptools import find_packages, setup
from setuptools.command.install import install
import subprocess
import os

class CustomInstall(install):
    def __init__(self, dist):
        super().__init__(dist)

    def run(self):
        install.run(self)
        self.__post_install()

    def __post_install(self):
        # Define the R packages to install
        r_packages = [
            'fst',
            'data.table',
            'readr',
            'aws.s3'
        ]

        # Get the current working directory
        curr = os.getcwd()

        # Iterate through the list of R packages and install them one by one
        for package in r_packages:
            if package == 'aws.s3':
                r_script = f"install.packages('{package}', repos='https://cloud.R-project.org')"
            else:
                r_script = f"install.packages('{package}', repos = 'https://cloud.r-project.org/')"
            try:
                process = subprocess.Popen(
                    ["Rscript", "-e", r_script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    cwd=curr  # Set the working directory for the R script
                )
                stdout, stderr = process.communicate()
                if process.returncode == 0:
                    print(f"Package '{package}' installed successfully.")
                else:
                    print(f"Error installing '{package}':")
                    print(stderr)
            except Exception as e:
                print("An error occurred:", str(e))


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()



setup(
    name='fstlib',
    packages= find_packages(),
    version='1.0.7',
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
    python_requires = ">=3.8",
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    cmdclass={'install': CustomInstall}
)