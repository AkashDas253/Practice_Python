
import json
import math
import os 
from typing import List, Dict, Optional 
from disk_driver import DiskDriver 

class FileSystem:
    """
    Manages the filesystem logic: metadata, file allocation, and operations.
    Relies on DiskDriver for all physical I/O.
    The filesystem is now hierarchical, with full paths as keys.
    """
    METADATA_BLOCK_ID = 0

    def __init__(self, disk: DiskDriver):
        self.disk = disk
        self.disk.init_disk()
        self.metadata = self._load_metadata()

        # Ensure the root directory always exists upon initialization
        if not self.metadata or "/" not in self.metadata:
            self.metadata["/"] = {'type': 'dir', 'size': 0, 'blocks': []}
            self._save_metadata() 

    # --- METADATA MANAGEMENT ---
    def _load_metadata(self) -> Dict:
        """Reads Block 0 to get the File Table (Superblock)."""
        raw_data = self.disk.read_block(self.METADATA_BLOCK_ID)
        clean_data = raw_data.rstrip(b'\x00')
        if not clean_data:
            return {}
        try:
            return json.loads(clean_data)
        except json.JSONDecodeError:
            print("[FS Error] Superblock data corrupted. Resetting.")
            return {}

    def _save_metadata(self):
        """Writes the File Table back to Block 0."""
        data = json.dumps(self.metadata).encode('utf-8')
        if len(data) > self.disk.BLOCK_SIZE:
            raise RuntimeError("Metadata size exceeded Block 0 capacity.")
        self.disk.write_block(self.METADATA_BLOCK_ID, data)

    # --- PATH and DIRECTORY HELPERS ---

    def _normalize_path(self, path: str) -> str:
        """Ensures paths start with / and removes trailing / unless it's the root."""
        path = os.path.normpath(path).replace('\\', '/')
        if not path.startswith('/'):
            path = '/' + path
        if len(path) > 1 and path.endswith('/'):
            path = path[:-1]
        return path

    def _resolve_path(self, path: str, target_type: Optional[str] = None) -> Optional[Dict]:
        """Looks up a full path in the metadata."""
        path = self._normalize_path(path)

        if path not in self.metadata:
            return None

        entry = self.metadata[path]
        if target_type and entry['type'] != target_type:
            return None 

        return entry
    
    def _add_entry(self, full_path: str, is_dir: bool, size: int = 0, blocks: List[int] = None):
        """Adds a new file or directory entry to the metadata."""
        full_path = self._normalize_path(full_path)
        
        if full_path in self.metadata:
            print(f"Error: Path '{full_path}' already exists.")
            return

        entry = {
            'type': 'dir' if is_dir else 'file',
            'size': size,
            'blocks': blocks if blocks is not None else []
        }
        self.metadata[full_path] = entry
        self._save_metadata()

    # --- ALLOCATION ---
    def _get_free_blocks(self, count: int) -> List[int]:
        """Calculates and reserves a list of free block IDs."""
        used_blocks = {self.METADATA_BLOCK_ID}
        for file_info in self.metadata.values():
            used_blocks.update(file_info['blocks'])

        free_blocks = []
        for i in range(1, self.disk.num_blocks):
            if i not in used_blocks:
                free_blocks.append(i)
                if len(free_blocks) == count:
                    return free_blocks
        
        raise MemoryError(f"Disk Full! Requested {count} blocks, but only {len(free_blocks)} available.")

    # --- FILE OPERATIONS ---
    def mkdir(self, path: str):
        """Creates a new directory."""
        path = self._normalize_path(path)
        if path == "/":
            print("Error: Root directory already exists.")
            return

        parent_path = self._normalize_path(os.path.dirname(path))
        if not self._resolve_path(parent_path, target_type='dir'):
            print(f"Error: Parent directory '{parent_path}' does not exist.")
            return

        self._add_entry(path, is_dir=True)
        print(f"Success: Created directory '{path}'")

    def ls(self, path: str = "/"):
        """List files and directories within a given path."""
        path = self._normalize_path(path)
        dir_entry = self._resolve_path(path, target_type='dir')
        if not dir_entry:
            print(f"Error: Directory '{path}' not found.")
            return

        print(f"\n--- Directory Listing for {path} ---")
        print(f"{'TYPE':<4} | {'NAME':<20} | {'SIZE':<8} | {'BLOCKS'}")
        print("-" * 55)

        found = False
        for full_name, info in self.metadata.items():
            if full_name == "/": continue

            parent_name = self._normalize_path(os.path.dirname(full_name))

            # Check if this entry is a direct child of the directory being listed
            if parent_name == path:
                print(f"{info['type'].upper():<4} | {os.path.basename(full_name):<20} | {info['size']:<8} | {info['blocks']}")
                found = True
            
        if not found and path != "/":
            print("(Empty directory)")
            
        print("\n")

    def import_file(self, host_path: str, target_path: str):
        """Imports a file from the host machine into the filesystem, checking path validity."""
        target_path = self._normalize_path(target_path)
        
        if self._resolve_path(target_path):
            print(f"Error: Path '{target_path}' already exists.")
            return

        parent_path = self._normalize_path(os.path.dirname(target_path))
        if not self._resolve_path(parent_path, target_type='dir'):
            print(f"Error: Parent directory '{parent_path}' does not exist.")
            return

        try:
            with open(host_path, 'rb') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: Local file '{host_path}' not found.")
            return

        num_blocks_needed = math.ceil(len(content) / self.disk.BLOCK_SIZE)
        
        try:
            block_ids = self._get_free_blocks(num_blocks_needed)
        except MemoryError as e:
            print(f"Error: {e}")
            return

        # Write data chunks to the allocated blocks
        for i, block_id in enumerate(block_ids):
            start = i * self.disk.BLOCK_SIZE
            end = start + self.disk.BLOCK_SIZE
            chunk = content[start:end]
            self.disk.write_block(block_id, chunk)

        # Update and save metadata using the new _add_entry
        self._add_entry(target_path, is_dir=False, size=len(content), blocks=block_ids)
        print(f"Success: Imported '{target_path}' using blocks {block_ids}")

    def cat(self, path: str):
        """Displays the content of a file."""
        path = self._normalize_path(path)
        file_entry = self._resolve_path(path, target_type='file')
        
        if not file_entry:
            print(f"Error: File '{path}' not found.")
            return
        
        info = file_entry
        full_data = b""
        
        for block_id in info['blocks']:
            full_data += self.disk.read_block(block_id)
            
        # Trim padding based on the exact recorded size
        actual_content = full_data[:info['size']]
        try:
            print(actual_content.decode('utf-8'))
        except UnicodeDecodeError:
            print("Content is binary and cannot be displayed.")

    def rm(self, path: str):
        """Removes a file or empty directory by deleting its metadata entry."""
        path = self._normalize_path(path)
        entry = self._resolve_path(path)

        if not entry:
            print(f"Error: Path '{path}' not found.")
            return

        if entry['type'] == 'dir':
            # Check if directory is empty before deleting
            path_prefix = path if path == "/" else path + "/"
            has_children = any(self._normalize_path(os.path.dirname(k)) == path for k in self.metadata if k != path)
            
            if has_children:
                print(f"Error: Cannot delete non-empty directory '{path}'.")
                return
        
        # Deleting the entry implicitly frees the blocks (if it's a file)
        del self.metadata[path]
        self._save_metadata()
        print(f"Success: Deleted '{path}' and freed its blocks.")