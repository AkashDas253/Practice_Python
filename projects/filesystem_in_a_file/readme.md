

# PyFS: A Filesystem in a File 

PyFS is a command-line utility built in Python that simulates a simple, **indexed, block-based filesystem** within a single host file. This project serves as a practical demonstration of low-level operating system concepts, including indexed block allocation, directory management, and metadata persistence.

## Features 

* **Block-Based Storage:** Data is organized into fixed-size **512-byte blocks**, mimicking physical disk sectors.
* **Hierarchical Directories:** Supports directory creation (`mkdir`) and navigation, structuring the file space.
* **Indexed Allocation (Block Maps):** Data blocks are no longer required to be contiguous. File metadata points to a **Block Map (Index Block)**, which in turn holds pointers to the file's data blocks.
* **Metadata Persistence:** A **Superblock (Block 0)** stores critical filesystem configuration. **Directory Blocks (Block 1 for Root)** store file/directory entries (metadata) as JSON, ensuring the structure is saved across sessions.
* **Separation of Concerns:** The code is structured into three distinct layers (Driver, Filesystem, CLI) for high modularity and maintainability.
* **Core File Operations:** Supports essential file and directory management commands.

---

## Memory Layout and Allocation Details 

The PyFS architecture reserves specific blocks for critical metadata and uses a dynamic allocation scheme for all other data. The total size and block count are defined in `config.json` and managed by the `DiskDriver`.

### Block Allocation Scheme

The disk is conceptually divided into three types of blocks:

| Block ID(s) | Role | Contents | Key Constants |
| :--- | :--- | :--- | :--- |
| **Block 0** | **Superblock** | System configuration, pointers to key structures. | `FileSystem.METADATA_BLOCK_ID` |
| **Block 1** | **Root Directory** | Directory entries (metadata) for files/folders in the root (`/`). | `FileSystem.ROOT_DIR_BLOCK_ID` |
| **Block 2+** | **Data Blocks** | Used for file data, **Block Maps (Index Blocks)**, and subdirectory contents. | Dynamic |

### 1. The Superblock (Block 0)

The Superblock is the foundation of the filesystem. It is saved as a **JSON object** and contains essential information required to mount the filesystem, such as the location of the root directory.

### 2. Directory Entries (Metadata)

Directories are stored in blocks (e.g., Block 1 for root). Each directory block can hold up to **4 entries** (`MAX_DIR_ENTRIES = 4`) because each entry is allocated **128 bytes** (`DIR_ENTRY_SIZE`) of space to store the file or directory's metadata as a padded JSON string.

* **File Entries** contain: `name`, `type: 'file'`, `size`, `num_blocks`, and `block_maps` (a list of Index Block IDs).
* **Directory Entries** contain: `name`, `type: 'dir'`, and `dir_block_id` (the ID of the block holding its own entries).

### 3. Indexed Allocation (Block Maps)

Instead of a File Allocation Table (FAT), PyFS uses a **Single-Level Indexing** mechanism via **Block Maps**.

1.  When a file is imported, the required data blocks and one or more **Index Blocks** (Block Maps) are allocated from the free space.
2.  The file's metadata stores the ID of the Index Block in its `block_maps` list.
3.  The Index Block itself is filled with **4-byte pointers** (`POINTER_SIZE` defined in `config.json`), where each pointer holds the ID of a data block belonging to the file.
4.  With a `BLOCK_SIZE` of 512 bytes and a `POINTER_SIZE` of 4 bytes, a single Index Block can point to **128 data blocks** (`POINTERS_PER_BLOCK`).

This design allows for files to use non-contiguous blocks, dramatically improving flexibility and reducing fragmentation compared to the original contiguous design.

## Architecture: Three-Layer Design 

The project employs a three-layer architecture to cleanly separate hardware abstraction from kernel logic.

| Layer | File | Role | Key Concepts |
| :--- | :--- | :--- | :--- |
| **1. Driver Layer** | `disk_driver.py` | **Hardware Abstraction:** Handles raw reading/writing of blocks. | Block Addressing, Padding, I/O, **Configuration Loading** |
| **2. Filesystem Layer** | `filesystem.py` | **Kernel Logic:** Manages the logical structure of files and free space. | **Indexed Allocation**, Superblock, Directory Entries, **Path Traversal** |
| **3. Interface Layer** | `pyfs_cli.py` | **User Interface:** Handles command-line parsing and system initialization. | Argument Routing |

## Getting Started

### Prerequisites

  * Python 3.6+
  * A `config.json` file in the same directory (containing `BLOCK_SIZE`, `NUM_BLOCKS`, etc.).

### Installation

No installation required. Ensure you have the following four files in the same directory:

1.  `config.json`
2.  `disk_driver.py`
3.  `filesystem.py`
4.  `pyfs_cli.py`

### Usage

All operations are run through the `pyfs_cli.py` script. The first argument is always the path to your disk image file (e.g., `my.dsk`).

#### Command Format

```bash
python pyfs_cli.py <DISK_FILE> <COMMAND> [ARGUMENTS...]
```

| Command | Description | Example |
| :--- | :--- | :--- |
| **`ls`** | Lists files, directories, sizes, and their allocated blocks. | `python pyfs_cli.py my.dsk ls /data` |
| **`mkdir`** | Creates a new directory. | `python pyfs_cli.py my.dsk mkdir /docs` |
| **`import`** | Copies a local file into PyFS. | `python pyfs_cli.py my.dsk import host_file.txt /docs/fs_name.txt` |
| **`cat`** | Reads and displays the content of a file from the virtual disk. | `python pyfs_cli.py my.dsk cat /docs/fs_name.txt` |
| **`rm`** | Deletes a file or an empty directory. | `python pyfs_cli.py my.dsk rm /docs/fs_name.txt` |

### Example Workflow

1.  **Create a local test file:**

    ```bash
    echo "Filesystem test data." > test.txt
    ```

2.  **Initialize, Create Directory, and List:**

    ```bash
    python pyfs_cli.py fs.img mkdir /data
    python pyfs_cli.py fs.img ls /
    ```

3.  **Import the file:**

    ```bash
    python pyfs_cli.py fs.img import test.txt /data/README.md
    ```

4.  **Verify content and list blocks:**

    ```bash
    python pyfs_cli.py fs.img cat /data/README.md
    python pyfs_cli.py fs.img ls /data
    ```

5.  **Remove the file:**

    ```bash
    python pyfs_cli.py fs.img rm /data/README.md
    python pyfs_cli.py fs.img ls /data
    ```

