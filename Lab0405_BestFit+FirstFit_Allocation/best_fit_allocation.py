
# Function to allocate memory to blocks 
def bestFit(blockSize, m, processSize, n): 
    
    # Stores block id of the block 
    # allocated to a process 
    allocation = [-1] * n 
    
    # pick each process and find suitable blocks according to its size and assign to it
    for i in range(n): 
        
        # Find the best fit block for current process 
        bestIdx = -1
        for j in range(m): 
            if blockSize[j] >= processSize[i]: 
                if bestIdx == -1: 
                    bestIdx = j 
                elif blockSize[bestIdx] > blockSize[j]: 
                    bestIdx = j 

        # If we could find a block for current process 
        if bestIdx != -1: 
            
            # allocate block j to p[i] process 
            allocation[i] = bestIdx 

            # Reduce available memory in this block. 
            blockSize[bestIdx] -= processSize[i] 

    print("\nProcess No.   Process Size     Block no.") 
    for i in range(n): 
        print(f" {i + 1} \t\t {processSize[i]} \t\t", end=" ") 
        if allocation[i] != -1: 
            print(allocation[i] + 1) 
        else: 
            print("Not Allocated") 
if __name__ == '__main__': 
    # 1. User inputs for Memory Blocks
    m = int(input("Enter the number of memory blocks: "))
    blockSize = []
    for i in range(m):
        size = int(input(f"Enter the size for Block {i + 1}: "))
        blockSize.append(size)

    # 2. User inputs for Processes
    n = int(input("\nEnter the number of processes: "))
    processSize = []
    for i in range(n):
        size = int(input(f"Enter the size for Process {i + 1}: "))
        processSize.append(size)

    # 3. Run the Algorithm
    print("\n--- Allocation Results ---")
    bestFit(blockSize, m, processSize, n)