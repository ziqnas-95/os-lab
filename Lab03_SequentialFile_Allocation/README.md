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

### 1. The Core Data Structure
- `self.disk` is an array representing a physical storage. Each index in the array is a block.
- `self.directory` is a simple map where the Key is the filename and the Value is address of the Index Block. 

### 2. How the Operations Work
#### A. File Creation (`create_file`)
When we create a file, the code needs N+1 blocks which includes the index block (where N is the file size)

- `get_free_blocks` picks random available indices from the disk
- The first block in that list is designated as the "Master" of that file (Index Block)
- Inside the Index Block, we store a list of all other block addresses where the data for the file is stored.

#### B. Reading a File
- The system looks at the directory to find the address of the Index Block.
- It goes to that address on the disk and retrieves the list of pointers.
- It now has the direct address of every single data block and can access them in any order (this is called Random Access).

#### C. Deleting a File
- Go to the Index Block.
- Use the pointers inside it to find every data block and set them to None (freeing them).
- Set the Index Block itself to None.
- Remove the filename from the directory.