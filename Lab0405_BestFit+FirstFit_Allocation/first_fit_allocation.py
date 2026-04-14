# 1. Initial Memory Setup
memory_blocks = [
    {"id": 1, "size": 100, "pid": None},
    {"id": 2, "size": 500, "pid": None},
    {"id": 3, "size": 200, "pid": None},
    {"id": 4, "size": 300, "pid": None},
    {"id": 5, "size": 600, "pid": None},
]

# 2. Core First-Fit Algorithm
def first_fit_allocate(pid, size):
    for block in memory_blocks:
        # Check if the block is empty AND big enough
        if block["pid"] is None and block["size"] >= size:
            block["pid"] = pid
            print(f"  [SUCCESS] '{pid}' placed in Block {block['id']}")
            return True
            
    print(f"  [FAILED] No suitable block for '{pid}'")
    return False

# 3. Display Function
def display_memory():
    print("\n--- Current Memory State ---")
    for b in memory_blocks:
        status = b["pid"] if b["pid"] else "Free"
        print(f"Block {b['id']} ({b['size']} KB) : {status}")
    print("----------------------------\n")

# 4. Main Program Loop
display_memory()

while True:
    pid = input("Enter Process ID (or type 'done'): ")
    if pid.lower() == 'done':
        break
        
    size = int(input(f"Enter size for {pid} (in KB): "))
    
    # Attempt to allocate, then show memory
    first_fit_allocate(pid, size)
    display_memory()