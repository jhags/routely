from setuptools import setup, find_packages

setup(
    name='routely',
    version='0.1.0',
    packages=find_packages(include=['routely', 'routely.*']),
    install_requires=open("requirements.txt").read(),
    tests_require=['unittest']
)
