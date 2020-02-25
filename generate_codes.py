import random
import string
import sqlite3
STRING_LENGTH = 30
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.sqlite3")

conn = sqlite3.connect(db_path)
c = conn.cursor()

def generate(count):
    codes = []
    for i in range(count):
        letters = string.ascii_letters
        unique_code = ''.join(random.choice(letters) for y in range(STRING_LENGTH))
        codes.append((unique_code))
        c.execute('INSERT INTO codes(code) VALUES (?)', (unique_code,))
    print(codes)
    conn.commit()
        


def main():
    print("Enter how many codes you want generated")
    i = int(input(" $ "))
    generate(i)

if __name__ == "__main__":
    main()