
import os
from typing import Optional

class DiskDriver:
    """
    Simulates a physical hard drive. 
    Handles raw block reading, writing, and file initialization.
    """
    BLOCK_SIZE = 512

    def __init__(self, disk_path: str, num_blocks: int = 50):
        self.disk_path = disk_path
        self.num_blocks = num_blocks

    def init_disk(self):
        """Creates the physical file full of zeros if it doesn't exist."""
        if os.path.exists(self.disk_path):
            return
        
        print(f"[Driver] Initializing new disk: {self.disk_path}")
        total_size = self.num_blocks * self.BLOCK_SIZE
        with open(self.disk_path, "wb") as f:
            f.write(b'\x00' * total_size) # Format with null bytes

    def read_block(self, block_id: int) -> bytes:
        """Reads a single block of data by its ID."""
        if block_id >= self.num_blocks or block_id < 0:
            raise IndexError(f"Block ID {block_id} is out of bounds.")
        
        with open(self.disk_path, "rb") as f:
            # Calculate physical offset and seek
            f.seek(block_id * self.BLOCK_SIZE)
            return f.read(self.BLOCK_SIZE)

    def write_block(self, block_id: int, data: bytes):
        """Writes data to a single block, padding if necessary."""
        if len(data) > self.BLOCK_SIZE:
            raise ValueError("Data exceeds block size.")
        if block_id >= self.num_blocks or block_id < 0:
            raise IndexError(f"Block ID {block_id} is out of bounds.")

        # Ensure we pad the data to exactly BLOCK_SIZE
        padded_data = data.ljust(self.BLOCK_SIZE, b'\x00')

        with open(self.disk_path, "r+b") as f:
            # Calculate physical offset and seek
            f.seek(block_id * self.BLOCK_SIZE)
            f.write(padded_data)