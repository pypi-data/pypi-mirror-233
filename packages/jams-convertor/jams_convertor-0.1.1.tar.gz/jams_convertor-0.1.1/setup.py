from setuptools import setup, find_packages

setup(
    name='jams_convertor',
    version='0.1.1',
    author='Bharath Radhakrishnan',
    author_email='bharathmsrk12@gmail.com',
    description='Converts JSON to JAMS format',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9.13',
)