from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A hello world package'
LONG_DESCRIPTION = 'A package that prints hello world in java'

setup(
    name="Javaworld",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Vishal",
    author_email="vishalvenkat2604@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='conversion',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
