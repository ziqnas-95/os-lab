"""
LAB 8: Dining Philosophers Problem
Deadlock Prevention: Asymmetric lock ordering
"""

import threading
import time

# ── INPUT ──────────────────────────────────────────
num_philosophers = int(input("Enter number of philosophers: "))
rounds           = int(input("Enter number of rounds: "))

chopsticks = [threading.Lock() for _ in range(num_philosophers)]
print_lock = threading.Lock()
log        = []


# ── SEQUENCE CONTROL ───────────────────────────────
# Each philosopher gets a personal "your turn" event
eating_order = [0, 2, 1, 3, 4]   # P1, P3, P2, P4, P5  (zero-indexed)

# One event per philosopher — set when it's their exact turn
turn_events = [threading.Event() for _ in range(num_philosophers)]

# Signals that a philosopher has fully finished eating (chopsticks released)
done_events = [threading.Event() for _ in range(num_philosophers)]

# Barrier to reset all events cleanly between rounds
round_barrier = threading.Barrier(num_philosophers)



# ── PROCESS ────────────────────────────────────────
def philosopher(pid):
    # Find this philosopher's position in the strict eating order
    my_position = eating_order.index(pid)

    left  = pid
    right = (pid + 1) % num_philosophers

    for r in range(1, rounds + 1):

        # Wait for your personal turn signal
        turn_events[pid].wait()
        turn_events[pid].clear()

        # Acquire chopsticks (asymmetric ordering retained)
        if pid % 2 == 1:
            first, second = left, right
        else:
            first, second = right, left

        chopsticks[first].acquire()
        chopsticks[second].acquire()

        # ── Eat ──
        msg = f"  Philosopher {pid + 1} is EATING (round {r}/{rounds})"
        with print_lock:
            print(msg)
            log.append(msg)
        time.sleep(0.5)

        chopsticks[left].release()
        chopsticks[right].release()

        # Mark self as done
        done_events[pid].set()

        # Signal the next philosopher in the order (if any)
        next_position = my_position + 1
        if next_position < len(eating_order):
            next_pid = eating_order[next_position]
            turn_events[next_pid].set()

        # Wait for ALL philosophers to finish this round
        round_barrier.wait()

        # Reset done events for next round
        done_events[pid].clear()

        # Barrier to ensure all resets complete
        round_barrier.wait()

        # First philosopher in order kicks off the next round
        if my_position == 0:
            turn_events[pid].set()

        # Final barrier so nobody races ahead
        round_barrier.wait()

        

# ── SPAWN THREADS ──────────────────────────────────
threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(num_philosophers)]

# Kick off the very first philosopher in the order
first_pid = eating_order[0]
turn_events[first_pid].set()

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

print("\nTable layout (clockwise):")
layout = " -- ".join(f"P{i+1} -- F{i+1}" for i in range(num_philosophers))
print(f"    {layout} -- [P1]")