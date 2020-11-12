from setuptools import setup, find_packages

setup(
    name='routely',
    version='0.1.0',
    packages=find_packages(include=['routely', 'routely.*']),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib'
    ],
    tests_require=['unittest']
)
