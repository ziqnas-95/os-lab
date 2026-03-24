# Indexed Allocation Flowchart and Pseudocode

This document describes the indexed allocation scheme implemented in `indexing-allocation.py`.

## Algorithm Summary

- Disk is an array of blocks of fixed size.
- Each file allocation needs one index block and `N` data blocks.
- Index block contains pointers to the data blocks.
- Directory maps filename -> index block.

## Pseudocode

```text
class IndexedAllocationSim:
    procedure __init__(disk_size=50):
        disk = array of disk_size set to None
        directory = empty map

    function get_free_blocks(count):
        free_indices = [i | i in 0..disk_size-1 and disk[i] is None]
        if len(free_indices) < count:
            return None
        return random_sample(free_indices, count)

    procedure create_file(filename, num_blocks):
        print "Creating", filename, "with", num_blocks, "data blocks"
        total_needed = num_blocks + 1  # one index block
        blocks = get_free_blocks(total_needed)
        if blocks is None:
            print "Error: Not enough free blocks"
            return

        index_block = blocks[0]
        data_blocks = blocks[1:]

        disk[index_block] = data_blocks
        for each address in data_blocks:
            disk[address] = "Data for " + filename

        directory[filename] = index_block
        print "File created successfully"

    procedure read_file(filename):
        if filename not in directory:
            print "Error: File not found"
            return

        index_block = directory[filename]
        pointers = disk[index_block]
        print "Index block", index_block, "pointers", pointers

        for each i, address in enumerate(pointers):
            print "Block", i, "@", address, ":", disk[address]

    procedure delete_file(filename):
        if filename not in directory:
            print "Error: File not found"
            return

        index_block = directory[filename]
        data_blocks = disk[index_block]

        for address in data_blocks:
            disk[address] = None

        disk[index_block] = None
        remove directory[filename]
        print "File deleted"
```

