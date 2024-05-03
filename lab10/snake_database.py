import psycopg2 as sql 

# connection to database 
connection=sql.connect(host = "localhost",
                       dbname = "postgres", 
                       user = "postgres", 
                       password = "Adil$notlove",
                       port = "5432" ) 
# it gives us access to database and we can merge data frome database
cursor = connection.cursor() 

cursor.execute("""
CREATE TABLE snake (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    score INTEGER NOT NULL,
    level INTEGER NOT NULL
);
""")

print("Hurray! Table is created")
connection.commit()

cursor.close()

connection.close