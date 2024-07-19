import hashlib
import time
import sqlite3


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


def write_block_to_db(conn, block):
    with conn:
        conn.execute("""
            INSERT INTO blockchain ("index", previous_hash, timestamp, data, hash)
            VALUES (?, ?, ?, ?, ?)
        """, (block.index, block.previous_hash, block.timestamp, block.data, block.hash))


def setup_database():
    conn = sqlite3.connect('block_chain.db')
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS blockchain (
                "index" INTEGER PRIMARY KEY,
                previous_hash TEXT,
                timestamp REAL,
                data TEXT,
                hash TEXT
            )
        """)
    return conn


def add_block(conn):
    cursor = conn.execute("SELECT * FROM blockchain ORDER BY \"index\" DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        previous_block = Block(row[0], row[1], row[2], row[3], row[4])
    else:
        previous_block = create_genesis_block()

    data = input("Enter data for the new block: ")
    new_block = create_new_block(previous_block, data)
    write_block_to_db(conn, new_block)
    print(f"Block #{new_block.index} has been added to the blockchain!")
    print(f"Hash: {new_block.hash}\n")


def read_blocks(conn):
    cursor = conn.execute("SELECT * FROM blockchain")
    for row in cursor:
        print(f"Index: {row[0]}")
        print(f"Previous Hash: {row[1]}")
        print(f"Timestamp: {row[2]}")
        print(f"Data: {row[3]}")
        print(f"Hash: {row[4]}\n")


def main():
    conn = setup_database()

    while True:
        print("Menu:")
        print("1 - Initialize database")
        print("2 - Add blockchain record")
        print("3 - Read blockchain records and print to screen")
        print("0 - Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            setup_database()
            print("Database initialized.\n")
        elif choice == '2':
            add_block(conn)
        elif choice == '3':
            read_blocks(conn)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()
