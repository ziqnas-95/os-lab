def bestFit(blockSize, m, processSize, n):
    originalBlockSize = blockSize[:]
    allocation = [-1] * n

    for i in range(n):
        bestIdx = -1
        for j in range(m):
            if blockSize[j] >= processSize[i]:
                if bestIdx == -1:
                    bestIdx = j
                elif blockSize[bestIdx] > blockSize[j]:
                    bestIdx = j

        if bestIdx != -1:
            allocation[i] = bestIdx
            blockSize[bestIdx] -= processSize[i]

    # --- Table Display ---
    col0 = 16  # Memory location
    col1 = 18  # Memory block size
    col2 = 14  # Job number
    col3 = 12  # Job size
    col4 = 10  # Status
    col5 = 22  # Internal fragmentation

    border = "+" + "-"*col0 + "+" + "-"*col1 + "+" + "-"*col2 + "+" + "-"*col3 + "+" + "-"*col4 + "+" + "-"*col5 + "+"

    def row(loc, blk, job, jsize, status, frag, pointer=""):
        prefix = f"{pointer:<2}"
        return (f"|{prefix}{str(loc):<{col0-2}}|{str(blk):<{col1}}"
                f"|{str(job):<{col2}}|{str(jsize):<{col3}}|{str(status):<{col4}}|{str(frag):<{col5}}|")

    print("\nMemory List:")
    print(border)
    print(row("Memory location", "Memory block size", "Job number", "Job size", "Status", "Internal fragmentation"))
    print(border)

    total_available = sum(originalBlockSize)
    total_used = 0

    for i in range(n):
        if allocation[i] != -1:
            blk_idx  = allocation[i]
            loc      = blk_idx + 1
            blk_size = f"{originalBlockSize[blk_idx]}K"
            job_no   = f"J{i + 1}"
            job_size = f"{processSize[i]}K"
            status   = "Busy"
            int_frag = f"{blockSize[blk_idx]}K"
            total_used += processSize[i]
            print(row(loc, blk_size, job_no, job_size, status, int_frag, pointer="->"))
        else:
            print(row("N/A", "N/A", f"J{i+1}", f"{processSize[i]}K", "Not Alloc.", "N/A"))

    # Free (unallocated) blocks
    allocated_blocks = set(allocation)
    for j in range(m):
        if j not in allocated_blocks:
            print(row(j + 1, f"{originalBlockSize[j]}K", "", "", "Free", ""))

    print(border)

    total_avail_str = f"Total Available: {total_available}K"
    total_used_str  = f"Total Used: {total_used}K"
    print(f"| {total_avail_str:<{col0+col1-1}} | {'':<{col2-1}}| {total_used_str:<{col3+col4+col5+2}}|")
    print(border)


if __name__ == '__main__':
    m = int(input("Enter the number of memory blocks: "))
    blockSize = []
    for i in range(m):
        size = int(input(f"  Size of Block {i + 1} (in K): "))
        blockSize.append(size)

    n = int(input("\nEnter the number of processes: "))
    processSize = []
    for i in range(n):
        size = int(input(f"  Size of Process {i + 1} (in K): "))
        processSize.append(size)

    print("\n--- Best Fit Allocation Results ---")
    bestFit(blockSize, m, processSize, n)