from setuptools import setup, find_packages

setup(
    name='klingon_serial',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'uuid',
        'datetime',
        'netifaces',
        'pytest',
        'setuptools'
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'console_scripts': [
            'klingon_serial=klingon_serial:main',
        ],
    },
)
