# bvzscanfilesystem

A python library to scan one or more directories (or a simple list of files) and return an object which contains a filtered dictionary of those same files where the key is the full path to the file, and the value is a list of attributes for that file.


This object also contains metrics like the number of skipped files (due to filtering rules) and numbers (and lists) of files that caused potential errors while scanning.

This library has no dependencies outside of Python 3.X

It was developed using python 3.10