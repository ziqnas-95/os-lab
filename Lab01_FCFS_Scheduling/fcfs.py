# ============================================================
# FCFS CPU Scheduling Simulator
# ============================================================

# Step 1: Get input from user
n = int(input("Enter number of processes: "))

burst = []  

for i in range(n):
    bt = int(input(f"Enter burst time for P{i+1}: "))
    burst.append(bt)

# Step 2: Calculate Completion Time
completion = []
time = 0

for bt in burst:
    time += bt             
    completion.append(time)

# Step 3: Calculate TAT and Waiting Time
arrival = 0   
tat     = [] 
waiting = [] 

for i in range(n):
    t = completion[i] - arrival       # TAT = CT - Arrival Time
    w = t - burst[i]                  # WT  = TAT - Burst Time
    tat.append(t)
    waiting.append(w)

# Step 4: Print results table
print("\n" + "-" * 65)
print(f"{'Process':<10} {'Burst':>8} {'CT':>8} {'TAT':>8} {'WT':>8}")
print("-" * 65)

for i in range(n):
    print(f"P{i+1:<9} {burst[i]:>8} {completion[i]:>8} {tat[i]:>8} {waiting[i]:>8}")

print("-" * 65)

# Step 5: Print averages
avg_tat = sum(tat) / n
avg_wt  = sum(waiting) / n

print(f"\nAverage Turnaround Time : {avg_tat:.2f}")
print(f"Average Waiting Time    : {avg_wt:.2f}")
