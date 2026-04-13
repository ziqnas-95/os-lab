import random

class SequentialAllocationSim:
    def __init__(self, disk_size=20):
        self.disk_size = disk_size
        self.disk = [None] * disk_size 
        self.directory = {}
        self.free_blocks = [True] * disk_size 
        self.file_counter = 1

    def _find_contiguous_space(self, length):
        for i in range(self.disk_size - length + 1):
            if all(self.free_blocks[i + j] for j in range(length)):
                return i
        return None

    def create_file(self, length):
        start_node = self._find_contiguous_space(length)
        if start_node is None:
            print(f"\n[!] Error: No contiguous gap of {length} blocks.")
            return

        filename = f"file{self.file_counter}"
        self.file_counter += 1

        for i in range(start_node, start_node + length):
            # Logical address is (i - start_node)
            logical_addr = i - start_node
            self.disk[i] = f"Data of '{filename}' (Logical Block {logical_addr})"
            self.free_blocks[i] = False

        self.directory[filename] = (start_node, length)
        print(f"\n[SUCCESS] '{filename}' allocated.")
        print(f"   Physical Range: Blocks {start_node} to {start_node + length - 1}")

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
                # We ask for a logical offset
                offset = int(input(f"Enter logical offset to read (0 to {length-1}): "))
                
                if 0 <= offset < length:
                    # The MATH that makes sequential allocation work:
                    physical_addr = start + offset
                    
                    print("-" * 40)
                    print(f"  LOGICAL ADDRESS  : {offset}")
                    print(f"  PHYSICAL ADDRESS : {physical_addr} (Start {start} + Offset {offset})")
                    print(f"  BLOCK CONTENT    : {self.disk[physical_addr]}")
                    print("-" * 40)
                else:
                    print(f"[!] Offset out of bounds. Must be 0 to {length-1}.")
            except ValueError:
                print("[!] Invalid input. Please enter a number.")
        else:
            print("[!] File not found.")

    def show_disk_map(self):
        print("\n" + "="*40)
        print(f"DISK MAP — {sum(self.free_blocks)}/{self.disk_size} blocks free")
        print("="*40)
        for i in range(0, self.disk_size, 5):
            indices = "  ".join([f"{idx:02d}" for idx in range(i, min(i+5, self.disk_size))])
            row = [" [ D ] " if not self.free_blocks[j] else " [ . ] " for j in range(i, min(i+5, self.disk_size))]
            print(f"  Addr : {indices}")
            print(f"  Disk :{''.join(row)}")
            print("  " + "-"*35)

def main():
    sim = SequentialAllocationSim(20)
    while True:
        print("\n1. Create\n2. Read (Logical vs Physical)\n3. Disk Map\n4. Exit")
        choice = input("Choice: ")
        if choice == '1':
            try:
                l = int(input("  File length: "))
                sim.create_file(l)
            except: pass
        elif choice == '2':
            sim.read_file_directly()
        elif choice == '3':
            sim.show_disk_map()
        elif choice == '4':
            break

if __name__ == "__main__":
    main()