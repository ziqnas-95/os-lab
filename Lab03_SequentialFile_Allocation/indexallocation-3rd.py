import random

class IndexedAllocationSim:
    def __init__(self, disk_size=20):
        """
        Initializes the simulated disk environment.
        - disk: A list representing physical storage blocks.
        - directory: A 'phonebook' mapping filenames to their Index Block address.
        - free_blocks: A set of indices not currently in use. Using a set makes 
          finding and removing blocks much faster (O(1)) than searching a list.
        """
        self.disk_size = disk_size
        self.disk = [None] * disk_size
        self.directory = {}
        self.free_blocks = set(range(disk_size))

    def _get_free_blocks(self, count):
        """
        Logic: Resource Allocation.
        This is a 'private' helper. It checks if the disk has enough room.
        If yes, it 'plucks' random indices from the free pool and returns them.
        Random sampling simulates how a disk becomes 'fragmented' over time.
        """
        if len(self.free_blocks) < count:
            return None
        
        # Select 'count' number of unique blocks from the available set
        allocated = random.sample(list(self.free_blocks), count)
        
        # Mark these as 'taken' by removing them from our free tracker
        for block in allocated:
            self.free_blocks.remove(block)
        return allocated

    def create_file(self, filename, num_blocks):
        """
        Logic: Metadata and Data Storage.
        1. Check if the name is unique (OS doesn't allow two 'notes.txt' in one folder).
        2. Calculate total space: 1 Index Block + N Data Blocks.
        3. Assign the first block as the 'Index'—this acts as the file's table of contents.
        4. Assign the rest as 'Data' blocks.
        """
        if filename in self.directory:
            print(f"\n[!] Error: File '{filename}' already exists.")
            return

        total_needed = num_blocks + 1
        blocks = self._get_free_blocks(total_needed)

        if not blocks:
            print(f"\n[!] Error: Disk full. Need {total_needed} blocks.")
            return

        # The 'Index Block' is like the brain of the file; it knows where everything is.
        index_addr = blocks[0]
        data_addrs = blocks[1:]

        # Store the 'pointers' (list of addresses) inside the physical index block
        self.disk[index_addr] = data_addrs
        
        # Fill the actual data blocks with simulated content
        for addr in data_addrs:
            self.disk[addr] = f"Content of {filename}"

        # Update the directory: Filename -> Address of the Index Block
        self.directory[filename] = index_addr
        print(f"\n[SUCCESS] '{filename}' created at Index Block {index_addr}.")

    def read_file(self, filename):
        """
        Logic: Indirect Access.
        In this method, we don't know where the data is initially. 
        We go to the Directory -> find the Index Block -> read the Pointers -> 
        finally jump to the Data Blocks. This is why it's called 'Indexed'.
        """
        if filename not in self.directory:
            print(f"\n[!] Error: File '{filename}' not found.")
            return
        
        # Step 1: Find where the 'table of contents' (Index Block) is
        index_addr = self.directory[filename]
        
        # Step 2: Read the pointers from that block
        pointers = self.disk[index_addr]

        print(f"\n--- Reading File: {filename} ---")
        print(f"Accessing Index Block {index_addr} to find data...")
        
        # Step 3: Follow each pointer to the physical data
        for i, addr in enumerate(pointers):
            print(f"  Block {i} (Addr {addr}): {self.disk[addr]}")

    def delete_file(self, filename):
        """
        Logic: Deallocation & Garbage Collection.
        To delete a file, we must clean up three things:
        1. The Data Blocks (set to None).
        2. The Index Block (set to None).
        3. The Directory Entry (remove the name).
        We also return all these addresses to the 'free_blocks' set so they can be reused.
        """
        if filename not in self.directory:
            print(f"\n[!] Error: File '{filename}' not found.")
            return

        index_addr = self.directory[filename]
        data_addrs = self.disk[index_addr]

        # Free data blocks back to the system
        for addr in data_addrs:
            self.disk[addr] = None
            self.free_blocks.add(addr)
        
        # Free the index block itself
        self.disk[index_addr] = None
        self.free_blocks.add(index_addr)

        # Wipe the file from the directory
        del self.directory[filename]
        print(f"\n[SUCCESS] File '{filename}' deleted. Blocks are now available.")

    def show_disk_map(self):
        """
        Logic: Visualization.
        This loops through the entire disk and creates a visual string.
        - [ . ] = Empty space.
        - [I:xx] = An Index block at address xx.
        - [ D ] = A block containing actual data.
        """
        print("\n" + "="*35)
        print(f"DISK STATUS: {len(self.free_blocks)}/{self.disk_size} FREE")
        print("="*35)
        
        display = []
        for i, val in enumerate(self.disk):
            if val is None:
                display.append("[ . ]")
            elif isinstance(val, list):
                display.append(f"[I:{i:02d}]") # Shows this is an Index block
            else:
                display.append("[ D ]")        # Shows this is a Data block

        # Print in clean rows of 5 for readability
        for start in range(0, self.disk_size, 5):
            end = min(start + 5, self.disk_size)
            indices = " ".join([f" {idx:02d} " for idx in range(start, end)])
            blocks = " ".join(display[start:end])
            print(f"Idx: {indices}")
            print(f"Sys: {blocks}\n" + "-"*35)

def main():
    """
    Logic: The User Interface Loop.
    This handles the 'human' side. It keeps the program running, 
    takes inputs, and translates them into method calls for the simulation.
    """
    print("Welcome to the OS File Allocation Simulator!")
    try:
        d_size = int(input("Enter disk capacity (blocks): "))
    except ValueError:
        d_size = 20 # Fallback if user enters text

    sim = IndexedAllocationSim(d_size)

    while True:
        print("\nMENU: [1] Create  [2] Read  [3] Delete  [4] Map  [5] Exit")
        choice = input("Select Option: ")

        if choice == '1':
            name = input("Name your file: ")
            try:
                size = int(input("How many data blocks? "))
                sim.create_file(name, size)
            except ValueError:
                print("Invalid size.")

        elif choice == '2':
            sim.read_file(input("Enter filename to read: "))

        elif choice == '3':
            sim.delete_file(input("Enter filename to delete: "))

        elif choice == '4':
            sim.show_disk_map()

        elif choice == '5':
            print("Shutting down... Goodbye!")
            break