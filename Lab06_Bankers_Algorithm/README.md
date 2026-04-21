# LAB 06 - Banker's Algorithm

## 6.1 Objective
Write a program to simulate Bankers algorithm for the purpose of deadlock avoidance.

## 6.2 Description
- In a multiprogramming environment, several processes may compete for a finite number of resources.
- A process requests resources; if the resources are not available at that time, the process enters a waiting state.
- Sometimes, a waiting process is never again able to change state, because the resources it has requested are held by other waiting processes. This situation is called a deadlock.

### Deadlock Avoidance
- One of the techniques for handling deadlocks is through the Banker's Algorithm. This approach requires that the operating system be given in advance additional information concerning which resources a process will request and use during its lifetime.
- With this additional knowledge, it can decide for each request whether or not the process should wait.
- To decide whether the current request can be satisfied or must be delayed, the system must consider the resources currently available, the resources currently allocated to each process, and the future requests and releases of each process.
- Banker's algorithm is a deadlock avoidance algorithm that is applicable to a system with multiple instances of each resource type.

---

## 6.3 How It Works

The Banker's Algorithm works like a bank that manages a limited pool of resources (devices). Before any process is allowed to start, it must declare the **maximum** number of resources it will ever need. The OS uses this information to decide whether granting a request keeps the system in a **safe state**.

### Key Concepts

| Term | Definition |
|------|-----------|
| **Allocation** | Number of devices currently held by a job |
| **Maximum** | The most devices a job will ever need to complete |
| **Need** | Remaining devices the job may still request (`Need = Max - Allocated`) |
| **Available** | Free devices the OS can hand out (`Available = Total - Sum of all Allocations`) |
| **Safe State** | A state where a safe sequence exists — every job can eventually finish |
| **Unsafe State** | No valid sequence exists — deadlock is possible |

### Safe vs Unsafe State

```
Safe State:   A safe sequence P1 → P2 → P3 exists where each job
              can get what it needs, finish, and release resources
              for the next job.

Unsafe State: No such sequence exists. At least one job will be
              permanently blocked waiting for resources that are
              held by other waiting jobs — this is deadlock.
```

### The Safety Algorithm

The safety algorithm simulates finishing every job using only the currently available resources. It does **not** change the real system state — it is purely a hypothetical check.

```
1. Set work = available devices
   Set finish[i] = False for all jobs

2. Find any unfinished job i where:
       need[i] <= work
   (the OS can satisfy this job right now)

3. If found:
       work = work + alloc[i]   (job finishes, releases devices)
       finish[i] = True
       Add job i to safe sequence
       Go back to step 2

4. If no job found in a full pass:
       UNSAFE — deadlock risk, break out of loop

5. If all jobs finished:
       SAFE — print the safe sequence
```

---

## 6.4 Program Flow

```
START
  |
  +--> Input: number of jobs, total devices
  |
  +--> For each job:
  |       Input: devices allocated, maximum required
  |       Validate: allocated <= maximum <= total devices
  |
  +--> Calculate:
  |       need[i]   = max[i] - allocated[i]
  |       available = total - sum(allocated)
  |
  +--> Print system state table
  |
  +--> Run Safety Algorithm
  |       |
  |       +--> SAFE?  --> Print safe sequence --> END
  |       |
  |       +--> UNSAFE? --> Print stuck jobs  --> END
```

---

## 6.5 Input Validation

The program includes three guards to prevent invalid system states:

| Guard | Condition | Error Message |
|-------|-----------|---------------|
| Guard 1 | `allocated > maximum` | Allocated cannot exceed Maximum |
| Guard 2 | `maximum > total_devices` | Maximum cannot exceed total devices in system |
| Guard 3 | `sum(allocated) > total_devices` | Total allocated exceeds total devices |

---

## 6.6 Sample Runs

### Scenario 1 — Safe State

**Input:**
```
Number of jobs    : 3
Total devices     : 12
Job 1 → Allocated: 3,  Max: 9
Job 2 → Allocated: 2,  Max: 3
Job 3 → Allocated: 4,  Max: 7
```

**System State Table:**
```
Job No.    | Devices Allocated    | Maximum Required     | Remaining Needs
---------------------------------------------------------------------------
Job 1      | 3                    | 9                    | 6
Job 2      | 2                    | 3                    | 1
Job 3      | 4                    | 7                    | 3
---------------------------------------------------------------------------
Total devices in system    : 12
Total devices allocated    : 9
Total devices available    : 3
```

**Safety Algorithm Trace:**
```
work = 3
Step 1: Job 2 — need 1 <= work 3  ✓  work = 3 + 2 = 5
Step 2: Job 3 — need 3 <= work 5  ✓  work = 5 + 4 = 9
Step 3: Job 1 — need 6 <= work 9  ✓  work = 9 + 3 = 12
All jobs finished.
```

**Output:**
```
State      : SAFE
Allocated  : 9 device(s)
Available  : 3 device(s)
Safe order : Job 2 → Job 3 → Job 1
```

---

### Scenario 2 — Unsafe State

**Input:**
```
Number of jobs    : 3
Total devices     : 10
Job 1 → Allocated: 4,  Max: 9
Job 2 → Allocated: 3,  Max: 6
Job 3 → Allocated: 2,  Max: 5
```

**System State Table:**
```
Job No.    | Devices Allocated    | Maximum Required     | Remaining Needs
---------------------------------------------------------------------------
Job 1      | 4                    | 9                    | 5
Job 2      | 3                    | 6                    | 3
Job 3      | 2                    | 5                    | 3
---------------------------------------------------------------------------
Total devices in system    : 10
Total devices allocated    : 9
Total devices available    : 1
```

**Safety Algorithm Trace:**
```
work = 1
Step 1: Job 1 — need 5 <= work 1  ✗  skip
        Job 2 — need 3 <= work 1  ✗  skip
        Job 3 — need 3 <= work 1  ✗  skip
No job found — no progress possible.
```

**Output:**
```
State      : UNSAFE — deadlock risk!
Allocated  : 9 device(s)
Available  : 1 device(s)
Stuck      : Job 1, Job 2, Job 3 cannot proceed
```

---

### Scenario 3 — Borderline Safe (4 Jobs)

**Input:**
```
Number of jobs    : 4
Total devices     : 15
Job 1 → Allocated: 2,  Max: 6
Job 2 → Allocated: 3,  Max: 7
Job 3 → Allocated: 4,  Max: 8
Job 4 → Allocated: 1,  Max: 5
```

**Output:**
```
State      : SAFE
Allocated  : 10 device(s)
Available  : 5 device(s)
Safe order : Job 1 → Job 2 → Job 3 → Job 4
```

> **Note:** Available is exactly 5 — just enough to satisfy the first job (need = 4).
> If available were 3 instead of 5, the state would be UNSAFE.

---

### Scenario 4 — Invalid Input Caught by Guard

**Input (user makes a mistake on Job 1):**
```
Number of jobs    : 2
Total devices     : 10
Job 1 → Allocated: 6,  Max: 4   ← INVALID
         ❌ Allocated (6) cannot exceed Maximum (4). Re-enter.
Job 1 → Allocated: 3,  Max: 8   ← corrected
Job 2 → Allocated: 3,  Max: 8
```

**Output:**
```
State      : UNSAFE — deadlock risk!
Allocated  : 6 device(s)
Available  : 4 device(s)
Stuck      : Job 1, Job 2 cannot proceed
```

---

## 6.7 Conclusion

The Banker's Algorithm is a **deadlock avoidance** strategy — not detection or recovery. It prevents the system from ever entering an unsafe state by checking every resource request before granting it. As long as all processes honestly declare their maximum needs and eventually release their resources, the algorithm guarantees the system will never deadlock.

