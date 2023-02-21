# bvzscanfilesystem

A python library to scan one or more directories (or a simple list of files) and return an object which contains a filtered dictionary of those same files where the key is the full path to the file, and the value is a list of attributes for that file.


This object also contains metrics like the number of skipped files (due to filtering rules) and numbers (and lists) of files that caused potential errors while scanning.

This library has no dependencies outside of Python 3.X

It was developed using python 3.10

Basic usage revolves around setting up a simple options object to hold the scan settings (things like whether to
skip certain types of files or directories, and optional regular expressions to filter out (or in) files or directories.

Then create a ScanFiles object and iterate over the directories and/or files you want to scan:

```
from bvzscanfilesystem.scanfiles import ScanFiles
from bvzscanfilesystem.options import Options

options_obj = Options(skip_sub_dir=False,
                      skip_hidden_files=False,
                      skip_hidden_dirs=False,
                      skip_zero_len=True,
                      incl_dir_regexes=None,
                      excl_dir_regexes=None,
                      incl_file_regexes=None,
                      excl_file_regexes=None,
                      report_frequency=10)

scan_obj = ScanFiles(scan_options=options_obj)

for counter in scan_obj.scan_directories(directories):
    print(f"Scanned {counter} files.")

for counter in scan_obj.scan_files(files_p=files, root_p="/"):
    print(f"Scanned {counter} files (doing loose files now)")
```