import random

class IndexedAllocationSim:
    def __init__(self, disk_size=20):
        self.disk_size = disk_size
        self.disk = [None] * disk_size
        self.directory = {}
        # Changed to a list to keep track of order easily
        self.free_blocks = [True] * disk_size 
        self.file_counter = 1

    def _get_contiguous_blocks(self, count):
        """Finds a starting index where 'count' blocks are free in a row."""
        for i in range(self.disk_size - count + 1):
            if all(self.free_blocks[i + j] for j in range(count)):
                # Mark them as taken
                for j in range(count):
                    self.free_blocks[i + j] = False
                return list(range(i, i + count))
        return None

    def create_file(self, num_blocks):
        # We need (1 index block + num_blocks data) all in a row
        total_needed = num_blocks + 1
        blocks = self._get_contiguous_blocks(total_needed)

        if not blocks:
            print(f"\n[!] Error: Could not find {total_needed} contiguous blocks.")
            print("    Even if the disk has space, it might be too fragmented!")
            return

        filename = f"file{self.file_counter}"
        self.file_counter += 1

        # Because they are contiguous:
        # blocks[0] is the Index
        # blocks[1:] are the data blocks (3, 4, 5...)
        index_addr = blocks[0]
        data_addrs = blocks[1:]

        self.disk[index_addr] = data_addrs

        for addr in data_addrs:
            self.disk[addr] = f"Data of '{filename}'"

        self.directory[filename] = index_addr
        print(f"\n[SUCCESS] '{filename}' created contiguously.")
        print(f"   Index Block : Block {index_addr}")
        print(f"   Data Blocks : {data_addrs} ")

    def read_index_block(self):
        if not self.directory:
            print("\n[!] No files created yet.")
            return

        print("\n--- Available Files & Index Blocks ---")
        for filename, addr in self.directory.items():
            print(f"{filename:<12} | Index: Block {addr}")
        print("-" * 35)

        while True:
            try:
                index_addr = int(input("  Enter index block to be read: "))
                if index_addr < 0 or index_addr >= self.disk_size:
                    raise ValueError
                if not isinstance(self.disk[index_addr], list):
                    print(f"  [!] Block {index_addr} is not an index block.")
                    continue
                break
            except ValueError:
                print("  [!] Invalid entry.")

        index_block = self.disk[index_addr]
        print(f"  Index Block {index_addr} points to: {index_block}")
        
        try:
            pos = int(input(f"  Enter position (1-{len(index_block)}): "))
            target = index_block[pos - 1]
            print(f"\n  Reading Block {target}: {self.disk[target]}")
        except (ValueError, IndexError):
            print("  [!] Invalid position.")

    def show_disk_map(self):
        print("\n" + "="*40)
        free_count = sum(self.free_blocks)
        print(f"DISK MAP  —  {free_count}/{self.disk_size} blocks free")
        print("="*40)

        for start in range(0, self.disk_size, 5):
            end = min(start + 5, self.disk_size)
            indices = "  ".join([f"{idx:02d}" for idx in range(start, end)])
            row = []
            for i in range(start, end):
                val = self.disk[i]
                if val is None: row.append("[ . ]")
                elif isinstance(val, list): row.append(f"[I:{i:02d}]")
                else: row.append("[ D ]")
            print(f"  Addr : {indices}")
            print(f"  Disk : {' '.join(row)}")
            print("  " + "-"*36)

def main():
    print("=" * 45)
    print("   Contiguous Indexed Allocation Simulator")
    print("=" * 45)
    d_size = 40
    sim = IndexedAllocationSim(d_size)

    while True:
        print("\n1. Create File\n2. Read Index\n3. Disk Map\n4. Exit")
        choice = input("Choice: ")
        if choice == '1':
            try:
                size = int(input("  Number of data blocks: "))
                sim.create_file(size)
            except ValueError: pass
        elif choice == '2': sim.read_index_block()
        elif choice == '3': sim.show_disk_map()
        elif choice == '4': break

if __name__ == "__main__":
    main()