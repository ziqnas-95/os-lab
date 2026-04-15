import random

class SequentialAllocationSim:
    def __init__(self, disk_size=20):
        self.disk_size = disk_size
        # Disk stores only data strings, no lists/pointers
        self.disk = [None] * disk_size 
        # Directory stores: { filename: (start_block, length) }
        self.directory = {}
        self.free_blocks = [True] * disk_size 
        self.file_counter = 1

    def _find_contiguous_space(self, length):
        """Standard sequential search for a 'hole' big enough for the file."""
        for i in range(self.disk_size - length + 1):
            if all(self.free_blocks[i + j] for j in range(length)):
                return i  # Return the starting index
        return None

    def create_file(self, length):
        start_node = self._find_contiguous_space(length)

        if start_node is None:
            print(f"\n[!] Error: No contiguous gap of {length} blocks available.")
            return

        filename = f"file{self.file_counter}"
        self.file_counter += 1

        # Allocate blocks physically in a row
        for i in range(start_node, start_node + length):
            self.disk[i] = f"Data of '{filename}' (Block {i-start_node})"
            self.free_blocks[i] = False

        # Directory ONLY stores start and length
        self.directory[filename] = (start_node, length)
        
        print(f"\n[SUCCESS] '{filename}' allocated sequentially.")
        print(f"   Start Block : {start_node}")
        print(f"   Length      : {length}")
        print(f"   Blocks Used : {list(range(start_node, start_node + length))}")

    def delete_file(self, filename):
        if filename not in self.directory:
            print(f"\n[!] Error: File '{filename}' not found.")
            return

        start, length = self.directory.pop(filename)

        # Clear the disk and free the blocks
        for i in range(start, start + length):
            self.disk[i] = None
            self.free_blocks[i] = True

        print(f"\n[DELETED] '{filename}' removed. Blocks {start} to {start + length - 1} are now free.")

    def read_file_directly(self):
        if not self.directory:
            print("\n[!] No files exist.")
            return

        print("\n--- Directory (Sequential) ---")
        print(f"{'Filename':<10} | {'Start':<6} | {'Length':<6}")
        for name, (start, length) in self.directory.items():
            print(f"{name:<10} | {start:<6} | {length:<6}")
        
        fname = input("\nEnter filename to read: ").strip()
        if fname in self.directory:
            start, length = self.directory[fname]
            try:
                offset = int(input(f"Enter relative block to read (0 to {length-1}): "))
                if 0 <= offset < length:
                    actual_addr = start + offset
                    print(f"\n[READ] Accessing Block {actual_addr} (Start {start} + Offset {offset})")
                    # print(f"Content: {self.disk[actual_addr]}")
                    # print(f"Content: Data {fname} (Relative Block: {offset}, Physical Block: {actual_addr})")
                    print(f"Data of Block {offset} of {fname} is stored at Physical Block: {actual_addr}")
                else:
                    print("[!] Offset out of bounds.")
            except ValueError:
                print("[!] Invalid input.")
        else:
            print("[!] File not found.")

    def show_disk_map(self):
        print("\n" + "="*40)
        free_count = sum(self.free_blocks)
        print(f"DISK MAP (Sequential) — {free_count}/{self.disk_size} free")
        print("="*40)
        for i in range(0, self.disk_size, 5):
            indices = "  ".join([f"{idx:02d}" for idx in range(i, min(i+5, self.disk_size))])
            blocks = " ".join(["[ 1 ]" if not self.free_blocks[j] else "[ 0 ]" for j in range(i, min(i+5, self.disk_size))])
            print(f"  Addr  : {indices}\n  Block : {blocks}\n  " + "-"*35)

def main():
    init_size = 20;
    sim = SequentialAllocationSim(init_size)
    print("\nSequential-File-Allocation-Simulator\nDisk Size of 20 is initialized.")

    while True:
        print("\n1. Create\n2. Read (Direct Access)\n3. Disk Map\n4. Delete File\n5. Exit")
        choice = input("Choice: ")
        if choice == '1':
            try:
                l = int(input("File length: "))
                sim.create_file(l)
            except: pass
        elif choice == '2': sim.read_file_directly()
        elif choice == '3': sim.show_disk_map()
        elif choice == '4': 
            fname = input("Enter filename to delete (e.g., file1): ").strip()
            sim.delete_file(fname)
        elif choice == '5': break

if __name__ == "__main__":
    main()