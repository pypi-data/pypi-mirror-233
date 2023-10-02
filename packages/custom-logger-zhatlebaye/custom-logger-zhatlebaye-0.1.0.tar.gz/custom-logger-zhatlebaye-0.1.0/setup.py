from setuptools import find_packages, setup

setup(
    name='custom-logger-zhatlebaye',
    packages=find_packages(include=['customLoggerZhatlebaye']),
    version='0.1.0',
    description='Custom logger',
    author='Adil, Bauka, Yerlan, Dimashka',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)