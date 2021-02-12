from setuptools import setup, find_packages

# requirement file
with open('requirements.txt') as f:
    required = f.read().splitlines()

# readme file
with open('README.rst') as f:
    readme = f.read()


setup(
    name='routely',
    version='0.1.3',
    description='Common operations and transformations on routes represented by a 2D line in xy space and corresponding z-axis data.',
    long_description=readme,
    long_description_content_type="text/x-rst",
    url='https://github.com/jhags/routely',
    author='J Hagstrom',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(include=['routely', 'routely.*']),
    install_requires=required,
    tests_require=['pytest', 'pytest-cov', 'coveralls'],
    python_requires='>=3.7',
)
