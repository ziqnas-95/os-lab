import random

class IndexedAllocationSim:
    def __init__(self, disk_size=50):
        self.disk = [None] * disk_size  # Simulate disk blocks
        self.disk_size = disk_size
        self.directory = {}  # filename -> list of block indices

    def get_free_blocks(self, count):
        free_indices = [i for i, block in enumerate(self.disk) if block is None]
        if len(free_indices) < count:
            return None  # Not enough free blocks
        return random.sample(free_indices, count)
    
    def create_file(self, filename, num_blocks):
        print(f"\n--- Creating File: '{filename}' ({num_blocks} data blocks) ---")

        # Need space for the data blocks plus one block for the index
        total_needed = num_blocks + 1  # +1 for the index block
        blocks = self.get_free_blocks(total_needed)

        if not blocks:
            print("Error: Not enough free space on disk to create the file.")
            return
        
        # Pick the first block as the index block and the rest as data blocks
        index_block_address = blocks[0]  # First block is the index block
        data_block_addresses = blocks[1:]  # Remaining blocks are data blocks

        # Allocate blocks on disk
        self.disk[index_block_address] = data_block_addresses  # Store data block addresses in index block
        for address in data_block_addresses:
            self.disk[address] = f"Data for {filename}"  # Simulate storing file data

        # Update directory with the filename and its index block address
        self.directory[filename] = index_block_address

        print(f"File created successfully.")
        print(f"Index block is at: {index_block_address}")
        print(f"Data blocks are at: {data_block_addresses}")


    def read_file(self, filename):
        print(f"\n--- Reading File: '{filename}' ---")
        if filename not in self.directory:
            print("Error: File not found.")
            return
        
        # Get the index block address from the directory
        index_block_address = self.directory[filename]

        # Read the data block addresses from the index block
        pointers = self.disk[index_block_address]  # Get data block addresses from index block

        print(f"Accessing index block {index_block_address}...")
        print(f"Found pointer to data blocks: {pointers}")

        # Fetch data using the pointers from the index block
        for i, address in enumerate(pointers):
            print(f"Reading from block {i} at Physical Address {address}: {self.disk[address]}")

    
    def show_disk_map(self):
        print("\n--- Disk Map ---")

        # Simple visualization of the disk blocks [I] for index blocks, [D] for data blocks, and . for free blocks
        display = []
        for i, val in enumerate(self.disk):
            if val is None:
                display.append("[.]")
            elif isinstance(val, list):
                display.append(f"[I:{i}]")
            else:
                display.append("[D]")

        # print(" ".join(display))
        # Print 5 blocks per line for readability
        chunk_size = 5
        for start in range(0, len(display), chunk_size):
            chunk = display[start:start + chunk_size]
            # also print the block indexes for clarity
            indexes = [f"{idx:02d}" for idx in range(start, min(start + chunk_size, len(display)))]
            print("Index:", " ".join(indexes))
            print("Blocks:", " ".join(chunk))
            print()

# --- Running the simulation ---
sim = IndexedAllocationSim(20)  # Create a disk with 20 blocks

# Create some files
sim.create_file("notes.txt", 3)  # Create a file that needs 3 data blocks + 1 index block
sim.create_file("photo.jpg", 5)  # Create another file that needs 5 data blocks + 1 index block

sim.show_disk_map()  # Show the disk map after file creation

# Retrieve a file
sim.read_file("notes.txt")  # Read the file we just created
sim.read_file("photo.jpg")  # Read the second file