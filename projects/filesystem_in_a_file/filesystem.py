
import json
import math
from typing import List, Dict
from disk_driver import DiskDriver 

class FileSystem:
    """
    Manages the filesystem logic: metadata, file allocation, and operations.
    Relies on DiskDriver for all physical I/O.
    """
    METADATA_BLOCK_ID = 0

    def __init__(self, disk: DiskDriver):
        self.disk = disk
        self.disk.init_disk() # Ensure the disk file exists
        self.metadata = self._load_metadata()

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
            # Handle corruption by returning empty state
            print("[FS Error] Superblock data corrupted. Resetting.")
            return {}

    def _save_metadata(self):
        """Writes the File Table back to Block 0."""
        data = json.dumps(self.metadata).encode('utf-8')
        if len(data) > self.disk.BLOCK_SIZE:
            raise RuntimeError("Metadata size exceeded Block 0 capacity.")
        self.disk.write_block(self.METADATA_BLOCK_ID, data)

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
    def ls(self):
        """List files and their info."""
        print(f"\n{'FILENAME':<15} | {'SIZE':<8} | {'BLOCKS'}")
        print("-" * 45)
        if not self.metadata:
            print("(Disk is empty)")
        for name, info in self.metadata.items():
            print(f"{name:<15} | {info['size']:<8} | {info['blocks']}")
        print("\n")

    def import_file(self, host_path: str, target_name: str):
        """Imports a file from the host machine into the filesystem."""
        if target_name in self.metadata:
            print(f"Error: File '{target_name}' already exists.")
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

        # Update and save metadata
        self.metadata[target_name] = {
            'size': len(content),
            'blocks': block_ids
        }
        self._save_metadata()
        print(f"Success: Imported '{target_name}' using blocks {block_ids}")

    def cat(self, filename: str):
        """Displays the content of a file."""
        if filename not in self.metadata:
            print(f"Error: File '{filename}' not found.")
            return
        
        info = self.metadata[filename]
        full_data = b""
        
        for block_id in info['blocks']:
            full_data += self.disk.read_block(block_id)
            
        # Trim padding based on the exact recorded size
        actual_content = full_data[:info['size']]
        try:
            print(actual_content.decode('utf-8'))
        except UnicodeDecodeError:
             print("Content is binary and cannot be displayed.")

    def rm(self, filename: str):
        """Removes a file by deleting its metadata entry."""
        if filename not in self.metadata:
            print(f"Error: File '{filename}' not found.")
            return
        
        # Deleting the entry implicitly frees the blocks (as they are no longer tracked)
        del self.metadata[filename]
        self._save_metadata()
        print(f"Success: Deleted '{filename}' and freed its blocks.")