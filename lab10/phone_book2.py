import psycopg2

def insert_contact(conn, username, phone_number):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO PhoneBook (username, phone_number) VALUES (%s, %s)", (username, phone_number))
    conn.commit()
    cursor.close()

def update_contact(conn, PhoneBook_id, new_username=None, new_phone_number=None):
    cursor = conn.cursor()
    if new_username:
        cursor.execute("UPDATE contacts SET username = %s WHERE id = %s", (new_username, PhoneBook_id))
    if new_phone_number:
        cursor.execute("UPDATE contacts SET phone_number = %s WHERE id = %s", (new_phone_number, PhoneBook_id))
    conn.commit()
    cursor.close()

def main():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Adil$notlove",
        host="localhost",
        port="5432"
    )

    username = input("Enter username: ")
    phone_number = input("Enter phone number: ")

    insert_contact(conn, username, phone_number)

    contact_id = input("Enter the ID of the contact to update: ")
    new_username = input("Enter the new username (leave blank to keep unchanged): ")
    new_phone_number = input("Enter the new phone number (leave blank to keep unchanged): ")
    update_contact(conn, contact_id, new_username, new_phone_number)

    conn.close()

if __name__ == "__main__":
    main()



