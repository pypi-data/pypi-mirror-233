"""
This file is used to install the package.
"""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
  
# Package metadata
name = 'table_transformer'
version = '1.0.2'
description = 'Table Transformer'
  
# Package dependencies
dependencies = [
    'onnxruntime~=1.14.1',
    'torchvision~=0.15.2',
    'numpy~=1.24',
    'pandas==1.5.3',
    'torch~=2.0.1',
    'matplotlib~=3.7.2',
    'seaborn~=0.12.0',
    'PyMuPDF==1.21.1',
    'scikit-image==0.20.0',
    'pathlib~=1.0.1',
    'pycocotools~=2.0.7',
    'editdistance==0.6.2',
    'scipy~=1.11.2',
    'Cython==0.29.33',
    'packaging~=23.1',
    'tqdm==4.65.0',
    'Pillow~=9.5.0',
    'wheel~=0.40.0',
]
  
# Package setup
setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=dependencies,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    include_package_data=True
)