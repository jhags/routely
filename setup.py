from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='routely',
    version='0.1.0',
    packages=find_packages(include=['routely', 'routely.*']),
    install_requires=required,
    tests_require=['pytest', 'pytest-cov', 'coveralls']
)
