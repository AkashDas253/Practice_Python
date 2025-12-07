

import argparse
from disk_driver import DiskDriver # DEPENDENCY
from filesystem import FileSystem # DEPENDENCY

def main():
    parser = argparse.ArgumentParser(description="PyFS: A Filesystem in a File CLI")
    
    # Global argument for the disk file path
    parser.add_argument("disk", help="Path to the disk image file (e.g., my.dsk)")
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Command: ls
    subparsers.add_parser("ls", help="List files on the disk")

    # Command: import <local_path> <fs_name>
    import_parser = subparsers.add_parser("import", help="Import a file from your host machine")
    import_parser.add_argument("src", help="Source file path on your host machine")
    import_parser.add_argument("dest", help="Destination filename in PyFS")

    # Command: cat <filename>
    cat_parser = subparsers.add_parser("cat", help="Display the content of a file")
    cat_parser.add_argument("file", help="Filename in PyFS to read")

    # Command: rm <filename>
    rm_parser = subparsers.add_parser("rm", help="Remove a file from the disk")
    rm_parser.add_argument("file", help="Filename in PyFS to delete")

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
        fs.ls()
    elif args.command == "import":
        fs.import_file(args.src, args.dest)
    elif args.command == "cat":
        fs.cat(args.file)
    elif args.command == "rm":
        fs.rm(args.file)

if __name__ == "__main__":
    main()