FIXED_BLOCKS = [
    {"block_no": 1, "size": 100, "pid": None},
    {"block_no": 2, "size": 500, "pid": None},
    {"block_no": 3, "size": 200, "pid": None},
    {"block_no": 4, "size": 300, "pid": None},
    {"block_no": 5, "size": 600, "pid": None},
]

def first_fit_allocate(blocks, pid, size):
    print(f"\n  Allocating '{pid}' ({size} KB) using First-Fit...")
    print(f"  Scanning blocks from Block 1...\n")
 
    for b in blocks:
        print(f"     Block {b['block_no']} ({b['size']} KB) -> ", end="")
 
        if b["pid"] is not None:
            print(f"Occupied by {b['pid']}, skip.")
            continue
 
        if b["size"] >= size:
            print(f"Free and fits! Allocating '{pid}' here.")
            b["pid"] = pid
            print(f"\n  [OK] '{pid}' allocated to Block {b['block_no']} ({b['size']} KB).")
            return True
        else:
            print(f"Free but too small ({b['size']} KB < {size} KB), skip.")
 
    print(f"\n  [FAILED] No suitable block found for '{pid}' ({size} KB).")
    return False

#MAIN PROGRAM
def main():
    blocks = [dict(b) for b in FIXED_BLOCKS]
    print("Initial Memory Blocks:")
    display_memory(blocks)
 
    while True:
        print("  Enter process details (or type 'done' to finish)\n")
 
        pid = input("  Process ID   : ").strip()
        if pid.lower() == "done":
            break
        if not pid:
            print("  Process ID cannot be empty.\n")
            continue
 
        if any(b["pid"] == pid for b in blocks):
            print(f"  '{pid}' is already allocated. Use a different name.\n")
            continue
 
        try:
            size = int(input("  Process Size (KB): "))
            if size <= 0:
                print("  Size must be greater than 0.\n")
                continue
        except ValueError:
            print("  Invalid size. Please enter a number.\n")
            continue
 
        first_fit_allocate(blocks, pid, size)
        display_memory(blocks)

        if all(b["pid"] is not None for b in blocks):
            print("  All memory blocks are now allocated. No space left.\n")
            break
 
    print("\n  FINAL MEMORY STATE ")
    display_memory(blocks)

#DISPLAY
def display_memory(blocks):
    print("\n  Memory Blocks:")
    for b in blocks:
        process = b["pid"] if b["pid"] else "---"
        status  = "Allocated" if b["pid"] else "Free"
        print(f"  {b['block_no']:<8} {str(b['size']) + ' KB':>12} {process:<12} {status:<12}")
    total     = sum(b["size"] for b in blocks)
    used      = sum(b["size"] for b in blocks if b["pid"])
    free      = total - used
    allocated = [b for b in blocks if b["pid"]]
 
    print(f"  Total Memory : {total} KB")
    print(f"  Used         : {used} KB")
    print(f"  Free         : {free} KB")
    print(f"  Processes    : {len(allocated)}")
   
if __name__ == "__main__":
    main()