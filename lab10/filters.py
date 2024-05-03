import psycopg2
import csv

conn = psycopg2.connect(
    dbname = "postgres",
    user = "postgres",
    password = "Adil$notlove",
    host = "localhost",
    port = "5432"
)

cur = conn.cursor()

def upload_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row_number, row in enumerate(reader, start=2):  # Start counting rows from 2 (after header)
            if len(row) < 2:
                print(f"Skipping row {row_number}: Not enough values")
                continue
            elif len(row) > 2:
                print(f"Skipping row {row_number}: Too many values")
                continue
            username, phone_number = row
            cur.execute("INSERT INTO PhoneBook (username, phone_number) VALUES (%s, %s)", (username, phone_number))
            conn.commit()


# Call the function with the path to your CSV file
upload_from_csv(r'C:\pp1\labs\aziza python\lab10\example.csv')

# Close the cursor and connection
cur.close()
conn.close()
