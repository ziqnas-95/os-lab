# ============================================================
# FCFS CPU Scheduling Simulator
# ============================================================

# Step 1: Get number of processes from user
n = int(input("Enter number of processes: "))

# List to store burst time of each process
burst = []

# Loop to input burst time for each process
for i in range(n):
    bt = int(input(f"Enter burst time for P{i+1}: "))
    burst.append(bt)   # store burst time in list

# Step 2: Calculate Completion Time (CT)
completion = []
time = 0  # keeps track of current CPU time

# FCFS: processes execute in the order entered
for bt in burst:
    time += bt                # add burst time of current process
    completion.append(time)   # store completion time

# Step 3: Calculate Turnaround Time (TAT) and Waiting Time (WT)
arrival = 0   # all processes arrive at time 0 (given in lab)
tat = []      # list to store turnaround times
waiting = []  # list to store waiting times

for i in range(n):
    # Turnaround Time = Completion Time - Arrival Time
    t = completion[i] - arrival
    
    # Waiting Time = Turnaround Time - Burst Time
    w = t - burst[i]
    
    tat.append(t)
    waiting.append(w)

# Step 4: Display results in table format
print("\n" + "-" * 65)
print(f"{'Process':<10} {'Burst':>8} {'CT':>8} {'TAT':>8} {'WT':>8}")
print("-" * 65)

# Print each process details
for i in range(n):
    print(f"P{i+1:<9} {burst[i]:>8} {completion[i]:>8} {tat[i]:>8} {waiting[i]:>8}")

print("-" * 65)

# Step 5: Calculate and display average times
avg_tat = sum(tat) / n   # average turnaround time
avg_wt  = sum(waiting) / n  # average waiting time

print(f"\nAverage Turnaround Time : {avg_tat:.2f}")
print(f"Average Waiting Time    : {avg_wt:.2f}")