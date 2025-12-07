import json
import math
import os
from typing import List, Dict, Optional, Set
from disk_driver import DiskDriver, CONFIG

# --- Constants ---
# Increased to 128 to accommodate JSON metadata overhead
DIR_ENTRY_SIZE = 128
MAX_DIR_ENTRIES = CONFIG['BLOCK_SIZE'] // DIR_ENTRY_SIZE

class FileSystem:
    METADATA_BLOCK_ID = 0
    ROOT_DIR_BLOCK_ID = 1

    def __init__(self, disk: DiskDriver):
        self.disk = disk
        self.superblock = self._load_superblock()
        
        if not self.superblock or 'root_dir_block_id' not in self.superblock:
            self.superblock = {'root_dir_block_id': self.ROOT_DIR_BLOCK_ID}
            self.disk.write_block(self.ROOT_DIR_BLOCK_ID, b'') 
            self._save_superblock()
            print(f"[FS] Formatted disk. Root at Block {self.ROOT_DIR_BLOCK_ID}.")
        
        self.fragmentation_check()

    # --- LOW LEVEL HELPERS ---
    def _load_superblock(self) -> Dict:
        raw_data = self.disk.read_block(self.METADATA_BLOCK_ID)
        clean_data = raw_data.rstrip(b'\x00')
        if not clean_data: return {}
        try:
            return json.loads(clean_data)
        except json.JSONDecodeError:
            return {}

    def _save_superblock(self):
        data = json.dumps(self.superblock).encode('utf-8')
        self.disk.write_block(self.METADATA_BLOCK_ID, data)

    def _read_dir_block(self, block_id: int) -> List[Dict]:
        data = self.disk.read_block(block_id)
        entries = []
        for i in range(MAX_DIR_ENTRIES):
            start = i * DIR_ENTRY_SIZE
            end = start + DIR_ENTRY_SIZE
            entry_bytes = data[start:end].rstrip(b'\x00')
            if entry_bytes:
                try:
                    entries.append(json.loads(entry_bytes.decode('utf-8')))
                except json.JSONDecodeError:
                    continue
        return entries

    def _write_dir_block(self, block_id: int, entries: List[Dict]):
        block_content = b''
        for entry in entries:
            entry_data = json.dumps(entry).encode('utf-8')
            if len(entry_data) > DIR_ENTRY_SIZE:
                # Critical check: ensure metadata fits in the slot
                raise ValueError(f"Entry '{entry.get('name')}' metadata too large ({len(entry_data)} > {DIR_ENTRY_SIZE}).")
            block_content += entry_data.ljust(DIR_ENTRY_SIZE, b'\x00')
        
        self.disk.write_block(block_id, block_content.ljust(self.disk.BLOCK_SIZE, b'\x00'))

    def _add_or_update_entry(self, parent_block_id: int, entry: Dict, is_new: bool):
        entries = self._read_dir_block(parent_block_id)
        
        if is_new and any(e['name'] == entry['name'] for e in entries):
            raise ValueError(f"Entry '{entry['name']}' already exists.")

        if is_new and len(entries) >= MAX_DIR_ENTRIES:
            raise MemoryError(f"Directory block {parent_block_id} is full (Max {MAX_DIR_ENTRIES} entries).")

        found = False
        for i, e in enumerate(entries):
            if e['name'] == entry['name']:
                entries[i] = entry
                found = True
                break
        
        if not found and is_new:
            entries.append(entry)
            
        self._write_dir_block(parent_block_id, entries)

    # --- ALLOCATION LOGIC ---
    def _calculate_used_blocks(self) -> Set[int]:
        used = {self.METADATA_BLOCK_ID}
        
        def traverse(dir_block):
            used.add(dir_block)
            for entry in self._read_dir_block(dir_block):
                if entry['type'] == 'dir':
                    traverse(entry['dir_block_id'])
                elif entry['type'] == 'file':
                    used.update(entry.get('block_maps', []))
                    used.update(self._get_data_blocks(entry))

        traverse(self.ROOT_DIR_BLOCK_ID)
        return used

    def _get_free_blocks(self, count: int) -> List[int]:
        used = self._calculate_used_blocks()
        free = []
        for i in range(2, self.disk.num_blocks):
            if i not in used:
                free.append(i)
                if len(free) == count:
                    return free
        raise MemoryError(f"Disk Full! Need {count}, found {len(free)}.")

    def _get_data_blocks(self, file_info: Dict) -> List[int]:
        data_blocks = []
        pointer_size = CONFIG['POINTER_SIZE']
        
        for map_id in file_info.get('block_maps', []):
            map_data = self.disk.read_block(map_id)
            for i in range(CONFIG['POINTERS_PER_BLOCK']):
                if len(data_blocks) >= file_info['num_blocks']:
                    return data_blocks
                
                start = i * pointer_size
                ptr_bytes = map_data[start:start+pointer_size]
                block_id = int.from_bytes(ptr_bytes, 'little')
                if block_id != 0:
                    data_blocks.append(block_id)
        return data_blocks

    def fragmentation_check(self):
        used = len(self._calculate_used_blocks())
        pct = used / self.disk.num_blocks
        if pct > CONFIG['DEFRAG_THRESHOLD']:
            print(f"[Warning] Disk Usage: {pct:.1%} (Threshold: {CONFIG['DEFRAG_THRESHOLD']:.1%})")

    # --- PATH OPERATIONS ---
    def _find_entry(self, path: str, target_type=None) -> Optional[Dict]:
        path = os.path.normpath(path).replace('\\', '/')
        if path == '/':
            return {'type': 'dir', 'dir_block_id': self.ROOT_DIR_BLOCK_ID}
        
        parts = [p for p in path.split('/') if p]
        curr_block = self.ROOT_DIR_BLOCK_ID
        curr_entry = None
        
        for i, part in enumerate(parts):
            entries = self._read_dir_block(curr_block)
            found = next((e for e in entries if e['name'] == part), None)
            
            if not found: return None
            
            curr_entry = found
            # Inject parent block ID so we can delete later
            curr_entry['parent_dir_block_id'] = curr_block 
            
            if i < len(parts) - 1:
                if found['type'] != 'dir': return None
                curr_block = found['dir_block_id']
        
        if target_type and curr_entry['type'] != target_type:
            return None
        return curr_entry

    # --- USER COMMANDS ---
    def mkdir(self, path: str):
        if self._find_entry(path):
            print(f"Error: '{path}' already exists.")
            return

        parent_path = os.path.dirname(path)
        parent = self._find_entry(parent_path, 'dir')
        if not parent:
            print(f"Error: Parent '{parent_path}' not found.")
            return

        try:
            block_id = self._get_free_blocks(1)[0]
            self.disk.write_block(block_id, b'') 
            
            new_entry = {
                'type': 'dir',
                'name': os.path.basename(path),
                'dir_block_id': block_id,
                'size': 0
            }
            self._add_or_update_entry(parent['dir_block_id'], new_entry, True)
            print(f"Directory '{path}' created.")
        except Exception as e:
            print(f"Mkdir failed: {e}")

    def import_file(self, src_path: str, dest_path: str):
        if self._find_entry(dest_path):
            print(f"Error: '{dest_path}' exists.")
            return
            
        try:
            with open(src_path, 'rb') as f: content = f.read()
        except FileNotFoundError:
            print("Host file not found.")
            return

        num_data_blocks = math.ceil(len(content) / self.disk.BLOCK_SIZE)
        num_map_blocks = math.ceil(num_data_blocks / CONFIG['POINTERS_PER_BLOCK'])
        
        if num_map_blocks > CONFIG['MAX_BLOCK_MAP_POINTERS']:
             print("File too large for configuration.")
             return

        try:
            needed = self._get_free_blocks(num_map_blocks + num_data_blocks)
            map_ids = needed[:num_map_blocks]
            data_ids = needed[num_map_blocks:]
        except MemoryError as e:
            print(f"Import failed: {e}")
            return

        # Write Data
        for i, bid in enumerate(data_ids):
            start = i * self.disk.BLOCK_SIZE
            chunk = content[start : start + self.disk.BLOCK_SIZE]
            self.disk.write_block(bid, chunk)

        # Write Map
        map_bytes = b''
        for bid in data_ids:
            map_bytes += bid.to_bytes(CONFIG['POINTER_SIZE'], 'little')
        self.disk.write_block(map_ids[0], map_bytes)

        # Update Dir
        parent = self._find_entry(os.path.dirname(dest_path), 'dir')
        if not parent:
            print("Error: Parent directory not found.")
            return

        entry = {
            'type': 'file',
            'name': os.path.basename(dest_path),
            'size': len(content),
            'block_maps': map_ids,
            'num_blocks': num_data_blocks
        }
        try:
            self._add_or_update_entry(parent['dir_block_id'], entry, True)
            print(f"Imported '{os.path.basename(dest_path)}'.")
        except ValueError as e:
            print(f"Error: {e}")

    def cat(self, path: str):
        entry = self._find_entry(path, 'file')
        if not entry:
            print(f"File '{path}' not found.")
            return
        
        data_ids = self._get_data_blocks(entry)
        full_data = b''
        for bid in data_ids:
            full_data += self.disk.read_block(bid)
        
        actual_data = full_data[:entry['size']]
        try:
            print(actual_data.decode('utf-8'))
        except:
            print("[Binary Data]")

    def ls(self, path: str):
        entry = self._find_entry(path, 'dir')
        if not entry:
            print(f"Directory '{path}' not found.")
            return
        
        print(f"\nListing: {path}")
        print(f"{'TYPE':<6} {'NAME':<15} {'SIZE':<8} {'BLOCKS'}")
        print("-" * 40)
        
        entries = self._read_dir_block(entry['dir_block_id'])
        if not entries:
            print("(Empty)")
            return

        for child in entries:
            if child['type'] == 'dir':
                blks = f"[{child['dir_block_id']}]"
            else:
                data_blks = self._get_data_blocks(child)
                blks = str(child['block_maps'] + data_blks)
            
            print(f"{child['type']:<6} {child['name']:<15} {child['size']:<8} {blks}")
        print()

    def rm(self, path: str):
        """Removes a file or empty directory."""
        entry = self._find_entry(path)
        if not entry:
            print(f"Error: '{path}' not found.")
            return

        if entry['type'] == 'dir':
            children = self._read_dir_block(entry['dir_block_id'])
            if children:
                print(f"Error: Directory '{path}' is not empty.")
                return
        
        # Parent Block ID was attached by _find_entry
        parent_block_id = entry.get('parent_dir_block_id')
        if parent_block_id is None:
            print("Error: Cannot delete root.")
            return

        # Rewrite parent directory block excluding this entry
        current_entries = self._read_dir_block(parent_block_id)
        new_entries = [e for e in current_entries if e['name'] != entry['name']]
        self._write_dir_block(parent_block_id, new_entries)
        
        print(f"Deleted '{path}'.")