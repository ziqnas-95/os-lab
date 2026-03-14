# LAB 08 - Dining Philosophers

## 8.1 Objective
Write a program to simulate the concept of Dining-Philosophers problem. 

## 8.2 Description
The dining-philosophers problem is considered a classic synchronization problem because it is an example of a 
large class of concurrency-control problems. It is a simple representation of the need to allocate several 
resources among several processes in a deadlock-free and starvation-free manner. 

### The Analogy
1. Consider five philosophers who spend their lives thinking and eating. 
2. The philosophers share a circular table surrounded by five chairs, each belonging to one philosopher. 
3. In the center of the table is a bowl of rice, and the table is laid with five single chopsticks. 
4. When a philosopher thinks, she does not interact with her colleagues. 
5. From time to time, a philosopher gets hungry and tries to pick up the two chopsticks that are closest to her (the chopsticks that are between her and her left and right neighbors). 
6. A philosopher may pick up only one chopstick at a time. 
7. Obviously, she cannot pick up a chopstick that is already in the hand of a neighbor. When a hungry philosopher has both her chopsticks at the same time, she eats without releasing her chopsticks. 
8. When she is finished eating, she puts down both of her chopsticks and starts thinking again.  

The dining-philosophers problem may lead to a deadlock situation and hence some rules have to be framed to avoid the occurrence of deadlock.

## 8.3 How it works...