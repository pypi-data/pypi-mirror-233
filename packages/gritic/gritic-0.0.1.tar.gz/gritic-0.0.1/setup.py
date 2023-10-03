from setuptools import setup

setup(
    name='gritic',
    version='0.0.1',
    packages=['gritic'],
    author='Toby Baker',
    author_email='toby.baker@crick.ac.uk',
    maintainer='Toby Baker',
    maintainer_email='toby.baker@crick.ac.uk',
    license='GNU AFFERO GENERAL PUBLIC LICENSE Version 3',
    url='https://github.com/VanLoo-lab/gritic',
    download_url='https://github.com/VanLoo-lab/gritic/archive/refs/tags/v0.0.1.tar.gz',
    description='A module to time complex copy number gains in cancer genomes',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        'sklearn',
        'networkx',
        'numba'
    ]
)

