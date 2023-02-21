from dataclasses import dataclass
import os


@dataclass
class Options:
    skip_sub_dir: bool = False
    skip_hidden_files: bool = False
    skip_hidden_dirs: bool = False
    skip_zero_len: bool = True
    incl_dir_regexes: (None, list) = None
    excl_dir_regexes: (None, list) = None
    incl_file_regexes: (None, list) = None
    excl_file_regexes: (None, list) = None
    report_frequency: int = 10
    uid: int = os.getuid()
    gid: int = os.getgid()
