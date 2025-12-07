import argparse
import sys
from disk_driver import DiskDriver
from filesystem import FileSystem

def main():
    parser = argparse.ArgumentParser(description="PyFS: Simulation Filesystem")
    parser.add_argument("disk", help="Path to disk file (e.g. segmented_test.dsk)")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # LS
    ls = subparsers.add_parser("ls")
    ls.add_argument("path", nargs='?', default='/')
    
    # MKDIR
    mk = subparsers.add_parser("mkdir")
    mk.add_argument("path")
    
    # IMPORT
    imp = subparsers.add_parser("import")
    imp.add_argument("src")
    imp.add_argument("dest")
    
    # CAT
    cat = subparsers.add_parser("cat")
    cat.add_argument("path")

    # RM (Added this)
    rm = subparsers.add_parser("rm")
    rm.add_argument("path")

    args = parser.parse_args()

    # Initialize
    try:
        driver = DiskDriver(args.disk)
        fs = FileSystem(driver)
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

    # Execute
    if args.command == "ls":
        fs.ls(args.path)
    elif args.command == "mkdir":
        fs.mkdir(args.path)
    elif args.command == "import":
        fs.import_file(args.src, args.dest)
    elif args.command == "cat":
        fs.cat(args.path)
    elif args.command == "rm":
        fs.rm(args.path)

if __name__ == "__main__":
    main()