''' This file was created in order to clean the data we have made about cities '''
import sqlite3

def find_duplicates(city_data):
    seen = set()
    duplicates = set()

    for city, data in city_data.items():
        city_key = (data['city'], data['country'])

        if city_key in seen:
            duplicates.add(city_key)
        else:
            seen.add(city_key)

    return duplicates

def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            country TEXT,
            weather TEXT,
            geography TEXT,
            continent TEXT
        )
    ''')

def insert_data(cursor, city_data):
    for city, data in city_data.items():
        cursor.execute('''
            INSERT INTO cities (city, country, weather, geography, continent)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['city'], data['country'], data['weather'], data['geography'], data['continent']))

def create_database(city_data):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('cities_database.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Drop the table if it exists
    cursor.execute('DROP TABLE IF EXISTS cities')

    # Create the table
    create_table(cursor)

    # Insert city data into the table
    insert_data(cursor, city_data)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print('Database created successfully.')
    print(f'Number of rows inserted: {len(city_data)}')

# Test the code
'''if __name__ == "__main__":

    # Check for duplicates
    duplicates = find_duplicates(city_data)

    if duplicates:
        print(f"Number of duplicates: {len(duplicates)}")
        print("Duplicate cities:")
        for duplicate in duplicates:
            print(f"{duplicate[0]}, {duplicate[1]}")
    else:
        print("No duplicates found.")

    # Create the database
    create_database(city_data)'''
