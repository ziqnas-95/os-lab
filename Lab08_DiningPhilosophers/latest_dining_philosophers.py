"""
LAB 8: Dining Philosophers Problem
Deadlock Prevention: Asymmetric lock ordering
"""

import threading
import time

# ── INPUT ──────────────────────────────────────────
num_philosophers = int(input("Enter number of philosophers: "))
rounds           = int(input("Enter number of rounds (times each philosopher eats): "))

chopsticks = [threading.Lock() for _ in range(num_philosophers)]
print_lock = threading.Lock()
barrier    = threading.Barrier(num_philosophers)  # sync all after each round
log = []

# ── PROCESS ────────────────────────────────────────
def philosopher(pid):
    left  = pid
    right = (pid + 1) % num_philosophers

    for r in range(1, rounds + 1):
        # Asymmetric lock ordering to prevent deadlock
        if pid % 2 == 1:
            first, second = left, right
        else:
            first, second = right, left

        chopsticks[first].acquire()
        chopsticks[second].acquire()

        msg = f"  Philosopher {pid + 1} is EATING (round {r}/{rounds})"
        with print_lock:
            print(msg)
            log.append(msg)
        time.sleep(0.5)

        chopsticks[left].release()
        chopsticks[right].release()

        # Wait for all philosophers to finish this round before continuing
        barrier.wait()

threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(num_philosophers)]

print("\n--- PROCESS ---")
for t in threads:
    t.start()
for t in threads:
    t.join()

# ── OUTPUT ─────────────────────────────────────────
print("\n--- OUTPUT ---")
print(f"Total philosophers : {num_philosophers}")
print(f"Rounds each        : {rounds}")
print(f"Total eating events: {len(log)}")
print("All philosophers ate successfully. No deadlock occurred.")

# Table layout
print("\nTable layout (clockwise):")
layout = " -- ".join(f"P{i+1} -- F{i+1}" for i in range(num_philosophers))
print(f"    {layout} -- [P1]")
