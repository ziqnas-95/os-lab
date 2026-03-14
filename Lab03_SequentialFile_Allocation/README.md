# LAB 03 - Sequential File Allocation

## 3.1 Objective
Write a program to simulate the indexed file allocation strategies. 

## 3.2 Description
- A file is a collection of data, usually stored on disk. As a logical entity, a file enables to divide data into meaningful groups. 
- As a physical entity, a file should be considered in terms of its organization.
- The term "file organization" refers to the way in which data is stored in a file and, consequently, the method(s) by which it can be accessed. 

### Indexed File Allocation
- Indexed file allocation strategy brings all the pointers together into one location: an index block. 
- Each file has its own index block, which is an array of disk-block addresses. 
- The i th entry in the index block points to the i th block of the file. 
- The directory contains the address of the index block. 
- To find and read the i th block, the pointer in the i th index-block entry is used. 

## 3.3 How it works...