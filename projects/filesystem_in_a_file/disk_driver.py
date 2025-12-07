import os
import json

# --- Configuration Loader ---
def load_config():
    """Loads configuration settings from config.json."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            # Calculate derived value: POINTERS_PER_BLOCK
            config['POINTERS_PER_BLOCK'] = config['BLOCK_SIZE'] // config['POINTER_SIZE']
            return config
    except FileNotFoundError:
        print("Error: config.json not found. Using default settings.")
        return {
            "BLOCK_SIZE": 512,
            "NUM_BLOCKS": 50,
            "DEFRAG_THRESHOLD": 0.50,
            "POINTER_SIZE": 4,
            "MAX_BLOCK_MAP_POINTERS": 1,
            "POINTERS_PER_BLOCK": 128 # 512 // 4
        }

CONFIG = load_config()

class DiskDriver:
    """
    Simulates a physical hard drive using a flat binary file.
    """
    BLOCK_SIZE = CONFIG['BLOCK_SIZE']

    def __init__(self, disk_path: str):
        self.disk_path = disk_path
        self.num_blocks = CONFIG['NUM_BLOCKS']
        self.init_disk()

    def init_disk(self):
        """Creates the physical file full of zeros if it doesn't exist."""
        if os.path.exists(self.disk_path):
            return
        
        print(f"[Driver] Initializing new disk: {self.disk_path} ({self.num_blocks} blocks)")
        total_size = self.num_blocks * self.BLOCK_SIZE
        with open(self.disk_path, "wb") as f:
            f.write(b'\x00' * total_size)

    def read_block(self, block_id: int) -> bytes:
        if block_id >= self.num_blocks or block_id < 0:
            raise IndexError(f"Block ID {block_id} is out of bounds.")
        
        with open(self.disk_path, "rb") as f:
            f.seek(block_id * self.BLOCK_SIZE)
            return f.read(self.BLOCK_SIZE)

    def write_block(self, block_id: int, data: bytes):
        if len(data) > self.BLOCK_SIZE:
            raise ValueError(f"Data size ({len(data)}) exceeds block size ({self.BLOCK_SIZE}).")
        if block_id >= self.num_blocks or block_id < 0:
            raise IndexError(f"Block ID {block_id} is out of bounds.")

        # Pad data with null bytes to fit the block exactly
        padded_data = data.ljust(self.BLOCK_SIZE, b'\x00')

        with open(self.disk_path, "r+b") as f:
            f.seek(block_id * self.BLOCK_SIZE)
            f.write(padded_data)