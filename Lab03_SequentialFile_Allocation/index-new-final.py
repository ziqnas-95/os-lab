import random


class IndexedAllocationSim:
    def __init__(self, disk_size=20):
        self.disk_size = disk_size
        self.disk = [None] * disk_size
        self.directory = {}
        self.free_blocks = set(range(disk_size))
        self.file_counter = 1

    def _get_free_blocks(self, count):
        if len(self.free_blocks) < count:
            return None
        allocated = random.sample(list(self.free_blocks), count)
        for block in allocated:
            self.free_blocks.remove(block)
        return allocated

    def create_file(self, num_blocks):
        total_needed = num_blocks + 1
        blocks = self._get_free_blocks(total_needed)

        if not blocks:
            print(f"\n[!] Disk full. Need {total_needed} blocks (1 index + {num_blocks} data).")
            return

        filename = f"file{self.file_counter}"
        self.file_counter += 1

        index_addr = blocks[0]
        data_addrs = blocks[1:]

        self.disk[index_addr] = data_addrs

        for addr in data_addrs:
            self.disk[addr] = f"Data of '{filename}'"

        self.directory[filename] = index_addr
        print(f"\n    '{filename}' successfully created.")
        print(f"    Index Block : Block {index_addr}")
        print(f"    Data Blocks : {data_addrs}")

    def read_index_block(self):
        while True:
            try:
                index_addr = int(input("Enter index block to be read: "))
            except ValueError:
                print("    [!] Invalid input. Enter a number.")
                continue

            if index_addr < 0 or index_addr >= self.disk_size:
                print(f"    [!] Invalid index block. Must be between 0 and {self.disk_size - 1}. Try again.")
                continue

            if not isinstance(self.disk[index_addr], list):
                print(f"    [!] Block {index_addr} is not an index block. Try again.")
                continue

            break

        index_block = self.disk[index_addr]
        num_data_blocks = len(index_block)

        print(f"    Index Block {index_addr} (array of pointers): {index_block}")

        while True:
            try:
                position = int(input(f"Enter block position to be read(1-{num_data_blocks}): "))
            except ValueError:
                print("     [!] Invalid input. Enter a number.")
                continue

            if position < 1 or position > num_data_blocks:
                print(f"    [!] Invalid position. Must be between 1 and {num_data_blocks}. Try again.")
                continue

            break

        target_addr = index_block[position - 1]
        print(f"\n    Entry {position} -> Block {target_addr:02d}: {self.disk[target_addr]}")

    def show_disk_map(self):
        print("\n" + "="*40)
        print(f"DISK MAP  —  {len(self.free_blocks)}/{self.disk_size} blocks free")
        print("="*40)

        display = []
        for i, val in enumerate(self.disk):
            if val is None:
                display.append("[ . ]")
            elif isinstance(val, list):
                display.append(f"[I:{i:02d}]")
            else:
                display.append("[ D ]")

        for start in range(0, self.disk_size, 5):
            end = min(start + 5, self.disk_size)
            indices = "  ".join([f"{idx:02d}" for idx in range(start, end)])
            blocks  = " ".join(display[start:end])
            print(f"  Addr : {indices}")
            print(f"  Disk : {blocks}")
            print("  " + "-"*36)


def main():
    print("=" * 39)
    print("   Indexed File Allocation Simulator")
    print("=" * 39)

    try:
        d_size = int(input("Enter disk size (number of blocks): "))
        if d_size < 2:
            raise ValueError
    except ValueError:
        print("Invalid input. Defaulting to 20 blocks.")
        d_size = 20

    sim = IndexedAllocationSim(d_size)

    while True:
        print("\n--- MENU ---")
        print("1. Create File")
        print("2. Read Index Block")
        print("3. Disk Map")
        print("4. Exit")
        choice = input("\nEnter choice: ").strip()

        if choice == '1':
            try:
                size = int(input("Enter number of data blocks: "))
                if size < 1:
                    raise ValueError
                sim.create_file(size)
            except ValueError:
                print("  [!] Invalid block count.")

        elif choice == '2':
            sim.read_index_block()

        elif choice == '3':
            sim.show_disk_map()

        elif choice == '4':
            print("\nShutting down simulator. Goodbye!")
            break

        else:
            print("  [!] Invalid option. Please choose 1–4.")

if __name__ == "__main__":
    main()