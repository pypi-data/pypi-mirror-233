from setuptools import setup, find_packages


setup(
    name='curveengine',
    version='1.1.5',
    description='A simple curve bootstraping tool based on ORE/QuantLib',
    long_description=open('readmepipy.md').read(),
    author='Jose Melo',
    package_data={
        "": ["*.py"]
    },
    author_email='jmelo@live.cl',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.9',
    install_requires=[
        'open-source-risk-engine']
)
