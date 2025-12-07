
# PyFS: A Filesystem in a File 

PyFS is a command-line utility built in Python that simulates a simple, block-based filesystem within a single host file. This project serves as a practical demonstration of low-level operating system concepts, including block allocation, metadata management, and persistence.

## Features

* **Block-Based Storage:** Data is organized into fixed-size 512-byte blocks, mimicking physical disk sectors.
* **Metadata Persistence:** A **Superblock (Block 0)** stores the File Allocation Table (FAT), ensuring files and structure are saved across reboots.
* **Contiguous Allocation:** Blocks are allocated sequentially to files for simplicity and efficient read/write.
* **Separation of Concerns:** The code is structured into three distinct layers (Driver, Filesystem, CLI) for high modularity and maintainability.
* **Core File Operations:** Supports essential file management commands.

## Architecture: Three-Layer Design

The project employs a three-layer architecture to cleanly separate hardware abstraction from kernel logic. 

| Layer | File | Role | Key Concepts |
| :--- | :--- | :--- | :--- |
| **1. Driver Layer** | `disk_driver.py` | **Hardware Abstraction:** Handles raw reading/writing of blocks. | Block Addressing, Padding, I/O |
| **2. Filesystem Layer** | `filesystem.py` | **Kernel Logic:** Manages the logical structure of files and free space. | Superblock, Metadata, Allocation |
| **3. Interface Layer** | `pyfs_cli.py` | **User Interface:** Handles command-line parsing and system initialization. | Argument Routing |

---

## Getting Started

### Prerequisites

* Python 3.6+

### Installation

No installation required. Ensure you have the following three files in the same directory:
1.  `disk_driver.py`
2.  `filesystem.py`
3.  `pyfs_cli.py`

### Usage

All operations are run through the `pyfs_cli.py` script. The first argument is always the path to your disk image file (e.g., `my.dsk`).

#### Command Format
```bash
python pyfs_cli.py <DISK_FILE> <COMMAND> [ARGUMENTS...]
```

| Command | Description | Example |
| :--- | :--- | :--- |
| **`ls`** | Lists files, sizes, and their allocated blocks. | `python pyfs_cli.py my.dsk ls` |
| **`import`** | Copies a local file into PyFS. | `python pyfs_cli.py my.dsk import host_file.txt fs_name.txt` |
| **`cat`** | Reads and displays the content of a file from the virtual disk. | `python pyfs_cli.py my.dsk cat fs_name.txt` |
| **`rm`** | Deletes a file's metadata entry (making its blocks free). | `python pyfs_cli.py my.dsk rm fs_name.txt` |

### Example Workflow

1.  **Create a local test file:**

    ```bash
    echo "Filesystem test data." | Out-File -Encoding UTF8 test.txt
    ```

2.  **Initialize and list files:**

    ```bash
    python pyfs_cli.py fs.img ls
    ```

3.  **Import the file:**

    ```bash
    python pyfs_cli.py fs.img import test.txt README.md
    ```

4.  **Verify content:**

    ```bash
    python pyfs_cli.py fs.img cat README.md
    ```
