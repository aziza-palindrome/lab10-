import psycopg2

def main():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Adil$notlove",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()

    # Retrieve all entries in the PhoneBook
    cursor.execute("SELECT * FROM PhoneBook")
    all_entries = cursor.fetchall()
    print("All entries in the PhoneBook:")
    for entry in all_entries:
        print(entry)

    # Retrieve entries with a specific username
    username = input("Enter the username to search: ")
    cursor.execute("SELECT * FROM PhoneBook WHERE username = %s", (username,))
    username_entries = cursor.fetchall()
    print(f"\nEntries with username '{username}':")
    for entry in username_entries:
        print(entry)

    # Retrieve entries with a specific phone number
    phone_number = input("Enter the phone number to search: ")
    cursor.execute("SELECT * FROM PhoneBook WHERE phone_number = %s", (phone_number,))
    phone_entries = cursor.fetchall()
    print(f"\nEntries with phone number '{phone_number}':")
    for entry in phone_entries:
        print(entry)

    # Delete an entry by username
    delete_username = input("Enter the username to delete: ")
    cursor.execute("DELETE FROM PhoneBook WHERE username = %s", (delete_username,))

    # Delete an entry by phone number
    delete_phone_number = input("Enter the phone number to delete: ")
    cursor.execute("DELETE FROM PhoneBook WHERE phone_number = %s", (delete_phone_number,))

    # Committing the changes and closing the cursor and connection
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
