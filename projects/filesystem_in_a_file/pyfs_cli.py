

import argparse
import sys 
from disk_driver import DiskDriver
from filesystem import FileSystem

def main():
    parser = argparse.ArgumentParser(description="PyFS: A Filesystem in a File CLI")
    
    # Global argument for the disk file path
    parser.add_argument("disk", help="Path to the disk image file (e.g., my.dsk)")
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Command: ls (Updated to accept an optional path)
    ls_parser = subparsers.add_parser("ls", help="List files on the disk or contents of a directory")
    ls_parser.add_argument("path", nargs='?', default='/', help="Optional directory path to list (default: /)")

    # Command: mkdir (New command)
    mkdir_parser = subparsers.add_parser("mkdir", help="Create a new directory")
    mkdir_parser.add_argument("path", help="The path of the directory to create (e.g., /user/docs)")

    # Command: import <local_path> <fs_path>
    import_parser = subparsers.add_parser("import", help="Import a file from your host machine")
    import_parser.add_argument("src", help="Source file path on your host machine")
    import_parser.add_argument("dest", help="Destination path in PyFS (e.g., /user/doc.txt)")

    # Command: cat <fs_path>
    cat_parser = subparsers.add_parser("cat", help="Display the content of a file")
    cat_parser.add_argument("path", help="Path of the file in PyFS to read")

    # Command: rm <fs_path>
    rm_parser = subparsers.add_parser("rm", help="Remove a file or empty directory from the disk")
    rm_parser.add_argument("path", help="Path of the file or directory to delete")

    args = parser.parse_args()

    # Initialize the System
    try:
        driver = DiskDriver(args.disk)
        fs = FileSystem(driver)
    except Exception as e:
        print(f"System Initialization Error: {e}")
        sys.exit(1)

    # Route Command Logic
    if args.command == "ls":
        fs.ls(args.path)
    elif args.command == "mkdir":
        fs.mkdir(args.path)
    elif args.command == "import":
        # Note: args.dest is used as the target path
        fs.import_file(args.src, args.dest) 
    elif args.command == "cat":
        fs.cat(args.path)
    elif args.command == "rm":
        fs.rm(args.path)

if __name__ == "__main__":
    main()