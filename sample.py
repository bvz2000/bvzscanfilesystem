#! /usr/bin/env python3

def get_user_input():
    """
    This function is used to get some data from the user. It is included in this sample just so that it is a fully
    functioning tool. It is not a necessary part of using this library.

    :return:
        A tuple containing a set of files and a set of directories to scan.
    """

    from argparse import ArgumentParser
    import os.path
    import sys

    # Read in an arbitrary list of query directories or files from the command line
    help_msg = "Scans an arbitrary list of files and/or directories, applying filters defined in the code."

    parser = ArgumentParser(description=help_msg)

    help_str = "The query directories or files. These are the directories and/or files that you want to scan."
    help_str += "Enter as many as you like."
    parser.add_argument('items',
                        metavar='items',
                        nargs="+",
                        type=str,
                        help=help_str)

    args = parser.parse_args(sys.argv)

    files = set()
    directories = set()

    for item in args.items:
        if os.path.isdir(item):
            directories.add(item)
        else:
            files.add(item)

    return files, directories


def do_scan(files: set, directories: set):
    """
    The code in this function is more or less the minimum code required to scan the filesystem using this library.

    :param files:
        A set containing any files to be included in the scan.
    :param directories:
        A set containing any directories to be included in the scan.

    :return:
        A ScanFiles obect.
    """

    from bvzscanfilesystem.scanfiles import ScanFiles
    from bvzscanfilesystem.options import Options

    # The ScanFiles object requires an Options object that holds all the filter settings.
    options_obj = Options(skip_sub_dir=False,
                          skip_hidden_files=False,
                          skip_hidden_dirs=False,
                          skip_zero_len=True,
                          incl_dir_regexes=None,
                          excl_dir_regexes=None,
                          incl_file_regexes=None,
                          excl_file_regexes=None,
                          report_frequency=10)

    # Create a ScanFiles object, passing it the options object
    scan_obj = ScanFiles(scan_options=options_obj)

    # Start by scanning any directories the user may have passed on the command line. The act of scanning is done via an
    # iterable, so that scan progress can be reported. The frequency of how often the function reports back (every N
    # files) is set in the Options object using the report_frequency argument.
    for counter in scan_obj.scan_directories(directories):
        print(f"Scanned {counter} files.")

    # Next scan any "loose" files the user may have included in their list of items. root_p is an arbitrary root path
    # that is stored with the scanned results in case a relative path to this arbitrary root needs to be referenced. The
    # root_p variable may be set to any arbitrary path, real or not. Scanning files is done more or less in the exact
    # same way as scanning directories. Note: the counter will continue to count from where it left off previously. In
    # fact, any additional scans will continue to add to the results of the previous scans. If you want to "reset" the
    # scan counter to zero or wipe clean any previously scanned files you will need to create a new ScanFiles object.
    for counter in scan_obj.scan_files(files_p=files, root_p="/"):
        print(f"Scanned {counter} files (doing loose files now)")

    return scan_obj


def print_results(scan_obj):
    """
    Prints up a simple report on the results of the scan.

    :param scan_obj:
        A ScanFiles object that has scanned the filesystem.

    :return:
        Nothing.
    """
    print("\n\n")
    print("Scan Settings:")
    print(f"Skip subdirectories: {scan_obj.options.skip_sub_dir}")
    print(f"Skip hidden files: {scan_obj.options.skip_hidden_files}")
    print(f"Skip hidden directories: {scan_obj.options.skip_hidden_dirs}")
    print(f"Skip zero length files: {scan_obj.options.skip_zero_len}")
    print(f"Include directory regexes: {scan_obj.options.incl_dir_regexes}")
    print(f"Exclude directory regexes: {scan_obj.options.excl_dir_regexes}")
    print(f"Include file regexes: {scan_obj.options.incl_file_regexes}")
    print(f"Exclude file regexes: {scan_obj.options.excl_file_regexes}")

    print("\n\n")
    print(f"Scanned {scan_obj.checked_count} files.")
    print(f"There were {scan_obj.skipped_links} skipped links.")
    print(f"There were {scan_obj.skipped_zero_len} skipped zero length files.")
    print(f"There were {scan_obj.skipped_hidden_files} skipped hidden files.")
    print(f"There were {scan_obj.skipped_hidden_dirs} skipped hidden directories.")
    print(f"There were {scan_obj.skipped_exclude_dirs} skipped directories because they were in the exclude regex.")
    print(f"There were {scan_obj.skipped_include_dirs} skipped directories because they were outside the include regex.")
    print(f"There were {scan_obj.skipped_exclude_files} skipped files because they were in the exclude regex.")
    print(f"There were {scan_obj.skipped_include_files} skipped files because they were outside the include regex.")

    print("\n")
    print(f"There were a total of {scan_obj.error_count} errors while scanning.")
    print(f"There were {len(scan_obj.file_permission_err_files)} file permission errors.")
    print("  ", end=None)
    print("\n  ".join(scan_obj.file_permission_err_files))

    print(f"There were {len(scan_obj.dir_permission_err_dirs)} directory permission errors.")
    print("  ", end=None)
    print("\n  ".join(scan_obj.dir_permission_err_dirs))

    print(f"There were {len(scan_obj.file_not_found_err_files)} file not found errors.")
    print("  ", end=None)
    print("\n  ".join(scan_obj.file_not_found_err_files))

    print(f"There were {len(scan_obj.file_generic_err_files)} generic file errors.")
    print("  ", end=None)
    print("\n  ".join(scan_obj.file_generic_err_files))

    print(f"There were {len(scan_obj.dir_generic_err_dirs)} generic directory errors.")
    print("  ", end=None)
    print("\n  ".join(scan_obj.dir_generic_err_dirs))


def main():
    files, directories = get_user_input()
    scan_obj = do_scan(files=files, directories=directories)
    print_results(scan_obj)


main()
