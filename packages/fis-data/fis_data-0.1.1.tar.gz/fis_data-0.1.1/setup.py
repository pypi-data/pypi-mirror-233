from setuptools import setup, find_packages

setup(
    name='fis_data',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
        'openpyxl',
    ],
    entry_points={
        'console_scripts': [
            'rearrange_fis_data=fis_data.rearrange_fis_data:main',
        ],
    },

    author='Naz Ebrahimi',
    description='A package for rearranging FIS data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NEbrahimi/fis_data',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
)
