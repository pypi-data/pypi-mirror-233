from setuptools import find_packages, setup

setup(
    name='fstlib',
    packages= find_packages(),
    version='0.1.0',
    description='R wrapper to handle fst files in pythoon',
    author='Vhiny-Guilley MOMBO',
    install_requires=["rpy2", "pandas", "numpy"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)