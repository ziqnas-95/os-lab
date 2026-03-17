
class IndexedFileSystem:
    def __init__(self):
        # Initialize the in-memory file metadata structures.
        # self.index: maps filename -> metadata (size, blocks locations)
        # self.files: maps filename -> actual content string
        self.index = {}
        self.files = {}
    
    def create_file(self, filename, content):
        # Create a file with a name and content.
        # Returns False if file exists, else True on success.
        if filename in self.files:
            print(f"File '{filename}' already exists")
            return False
        
        self.files[filename] = content
        self.index[filename] = {
            'size': len(content),  # length of content in bytes/characters
            'blocks': self._allocate_blocks(filename, content)  # logical block mapping
        }
        return True
    
    def _allocate_blocks(self, filename, content):
        # Internal helper: divide content into fixed-size blocks.
        # Returns list of block metadata dicts with block_id and offset.
        block_size = 64
        blocks = []
        for i in range(0, len(content), block_size):
            # Each block description includes its index and offset into the file's content.
            blocks.append({'block_id': len(blocks), 'offset': i})
        return blocks
    
    def search_file(self, filename):
        # Return file metadata from index for a given filename.
        # Returns None if file is not found.
        return self.index.get(filename, None)
    
    def delete_file(self, filename):
        # Remove file data and metadata for the given filename.
        # Returns True if deletion succeeded, False if file did not exist.
        if filename in self.files:
            del self.files[filename]
            del self.index[filename]
            return True
        return False
    
    def list_files(self):
        # Return list of filenames currently stored in the indexed file system.
        return list(self.index.keys())


# Example usage
if __name__ == "__main__":
    fs = IndexedFileSystem()
    fs.create_file("file1.txt", "Hello World")
    fs.create_file("file2.txt", "Python file system")
    print("Files:", fs.list_files())
    print("File1 info:", fs.search_file("file1.txt"))