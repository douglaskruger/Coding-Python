import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = f"{index}{previous_hash}{timestamp}{data}".encode()
    return hashlib.sha256(value).hexdigest()

def create_genesis_block():
    timestamp = time.time()
    return Block(0, "0", timestamp, "Genesis Block", calculate_hash(0, "0", timestamp, "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    previous_hash = previous_block.hash
    hash = calculate_hash(index, previous_hash, timestamp, data)
    return Block(index, previous_hash, timestamp, data, hash)

def main():
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0]

    num_blocks_to_add = 5
    for i in range(num_blocks_to_add):
        new_block_data = f"Block #{i + 1} data"
        new_block = create_new_block(previous_block, new_block_data)
        blockchain.append(new_block)
        previous_block = new_block
        print(f"Block #{new_block.index} has been added to the blockchain!")
        print(f"Hash: {new_block.hash}\n")

if __name__ == "__main__":
    main()
