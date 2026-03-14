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
- Banker’s algorithm is a deadlock avoidance algorithm that is applicable to a system with multiple instances of each resource type.

## 6.3 How it works...