# sonar
Sonar signal processing library

This is an experimental library for sonar signal processing purposes

The main idea of this library is to unify the processing applied to sonar system signals from labsonar and lps.

## Structure
Both matlab and python maintain the same general directory structure.
- **labsonar_sp**: with the files needed to use the library.
- **test**: file(s) with unit tests of the library's functionalities.
As a general recommendation, run unit tests before submitting

## matlab
In matlab, the test applications assume they are running in the root directory (sonar / git home). To use the library features, run the command:
```
addpath("matlab/labsonar_sp)"
```
The generate_ref_files.m file generates all files from the test_data folder, reference files for unit tests in python and matlab. This file should only be executed when adding new functionalities or modifying the functioning of any of the pre-existing functions

## python
To install the labsonar_sp library, enter the python folder and run the command
```
pip install -e .
```
