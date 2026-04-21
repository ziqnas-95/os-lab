# ============================================================
# FCFS CPU Scheduling Simulator (Non-Preemptive)
# ============================================================

# Step 1: Get number of processes from user
n = int(input("Enter number of processes: "))

# Lists to store arrival time (AT) and burst time (BT)
arrival = []
burst = []

# ------------------------------------------------------------
# Step 2: Input arrival time and burst time for each process
# ------------------------------------------------------------
for i in range(n):
    at = int(input(f"Enter arrival time for P{i+1}: "))
    bt = int(input(f"Enter burst time for P{i+1}: "))
    
    arrival.append(at)
    burst.append(bt)

# ------------------------------------------------------------
# Step 3: Sort processes based on arrival time (FCFS rule)
# ------------------------------------------------------------
# Combine arrival time, burst time, and process index together
# This helps us sort while still keeping track of process number
processes = list(zip(arrival, burst, range(n)))

# Sort processes by arrival time (first element of tuple)
processes.sort(key=lambda x: x[0])

# Separate sorted values back into individual lists
arrival = [p[0] for p in processes]
burst = [p[1] for p in processes]
order = [p[2] for p in processes]  # original process numbers

# ------------------------------------------------------------
# Step 4: Initialize lists for results
# ------------------------------------------------------------
completion = []   # Completion Time (CT)
tat = []          # Turnaround Time (TAT)
waiting = []      # Waiting Time (WT)

time = 0  # Keeps track of current CPU time

# ------------------------------------------------------------
# Step 5: Calculate CT, TAT, and WT using FCFS algorithm
# ------------------------------------------------------------
for i in range(n):
    
    # If CPU is idle and next process has not arrived yet,
    # move time forward to that process's arrival time
    if time < arrival[i]:
        time = arrival[i]
    
    # Add burst time of current process to current time
    time += burst[i]
    
    # Completion Time = current time after execution
    completion.append(time)
    
    # Turnaround Time = Completion Time - Arrival Time
    tat.append(completion[i] - arrival[i])
    
    # Waiting Time = Turnaround Time - Burst Time
    waiting.append(tat[i] - burst[i])

# ------------------------------------------------------------
# Step 6: Display results in tabular format
# ------------------------------------------------------------
print("\n" + "-" * 65)
print(f"{'Process':<10} {'AT':>8} {'BT':>8} {'CT':>8} {'TAT':>8} {'WT':>8}")
print("-" * 65)

# Print each process result
for i in range(n):
    print(f"P{order[i]+1:<9} {arrival[i]:>8} {burst[i]:>8} {completion[i]:>8} {tat[i]:>8} {waiting[i]:>8}")

print("-" * 65)

# ------------------------------------------------------------
# Step 7: Calculate and display averages
# ------------------------------------------------------------
avg_tat = sum(tat) / n
avg_wt = sum(waiting) / n

print(f"\nAverage Turnaround Time : {avg_tat:.2f}")
print(f"Average Waiting Time    : {avg_wt:.2f}")