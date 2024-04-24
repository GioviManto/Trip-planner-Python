''' This file works with the database and it is our server side of what will be displayed
    in our client side if the user doesn't know where to go.
 
    The database is made by us using AI in order to generate data, we've payed attention on
    the consistency of the data, but for 4092 cities is hard to say that there is no error '''

import sqlite3
import os

# Function to get user credentials
def get_user_credentials():
    username = input("Insert your username: ")
    password = input("Insert your password: ")
    return username, password

# Function to connect to the SQLite database
def connect_to_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        print("Database connected successfully.")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")

# Function to get the SQLite database connection and cursor
def get_db_connection():
    print("Getting database connection")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print("Your database is in this directory: ", script_dir)
    db_path = os.path.abspath(os.path.join(script_dir, 'cities_database.db'))
    print("Database path: ", db_path)

    try:
        conn = connect_to_database(db_path)
        if conn:
            cursor = conn.cursor()
            return conn, cursor
        else:
            print("Failed to get the database connection.")
            return None, None
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None, None



# Function to close the database connection
def close_connection(conn):
    if conn:
        conn.close()

# Function to get the continent for travel advice
def get_continent_for_advice():
    continents = ['Asia', 'Europe', 'North America', 'South America', 'Oceania', 'Africa']
    while True:
        continent = input(f"Of which continent are you dreaming? {', '.join(continents)}: ")
        if continent.capitalize() in continents:
            return continent.capitalize()
        else:
            print("Invalid continent. Please choose from the provided options.")

# Function to get a list of countries for a given continent
def get_countries_per_continent(cursor, continent):
    try:
        cursor.execute('SELECT DISTINCT country FROM cities WHERE continent=? ORDER BY country', (continent,))
        country_list = [country[0] for country in cursor.fetchall()]
        return country_list
    except sqlite3.Error as e:
        print("Error retrieving countries:", e)
        return []

# Function to get a user-selected country for travel advice
def get_country_for_advice(countries):
    print("Our recommended countries for this continent are:")
    for country in countries:
        print(country)
    while True:
        country_input = input("\nChoose one country from the list above: ")
        if country_input in countries:
            return country_input
        else:
            print("Invalid country. Please choose from the provided options.")

# Function to get all the cities in a country
def get_city_per_country_in_continent(cursor, country):
    try:
        cursor.execute('SELECT DISTINCT city FROM cities WHERE country=?', (country,))
        city_list = [city[0] for city in cursor.fetchall()]
        return city_list
    except sqlite3.Error as e:
        print("Error retrieving countries:", e)
        return []


# Function to get the preferred weather for travel advice
def get_weather_for_advice():
    weather_options = ['temperate', 'hot', 'cold']
    while True:
        weather = input("Which weather would you like to find? (temperate/hot/cold) ")
        if weather.lower() in weather_options:
            return weather.lower()
        else:
            print("Invalid weather. Please choose from the provided options.")

# Function to get cities with a specific weather in a given country
def get_city_per_weather_in_country(cursor, weather, country):
    try:
        cursor.execute('''SELECT DISTINCT city FROM cities WHERE Weather = ? AND Country = ?''', (weather, country))
        mylist = cursor.fetchall()
        result = [city[0] for city in mylist]
        return result
    except sqlite3.Error as e:
        print("Error retrieving cities:", e)
        return None

# Function to get the preferred geography for travel advice
def get_geography_for_advice():
    geography_options = ['urban','coastal', 'mountainous']
    while True:
        geography = input("Do you prefer desert, urban, mountainous or coastal? (urban/coastal/mountainous) ")
        if geography.lower() in geography_options:
            return geography.lower()
        else:
            print("Invalid geography. Please choose from the provided options.")

# Function to get cities with a specific geography in a given country
def get_city_per_geography_in_country(cursor, geography, country):
    try:
        cursor.execute('''SELECT DISTINCT city FROM cities WHERE Geography = ? AND Country = ?''', (geography, country))
        mylist = cursor.fetchall()
        result = [city[0] for city in mylist]
        return result
    except sqlite3.Error as e:
        print("Error retrieving cities:", e)
        return None

# Function to get cities with a specific geography and weather in a given country
def get_city_per_geography_and_weather_in_country(cursor, geography, weather, country, offset=0, limit=5): # The defualt number of recommended cities as output will be 5
    try:
        cursor.execute('''
            SELECT DISTINCT city 
            FROM cities 
            WHERE Geography = ? AND Weather = ? AND Country = ?
            LIMIT ? OFFSET ?
        ''', (geography, weather, country, limit, offset))
        mylist = cursor.fetchall()
        result = [city[0] for city in mylist]
        return result
    except sqlite3.Error as e:
        print("Error retrieving cities:", e)
        return None

## Function to provide travel advice based on user preferences
def advice_with_db(conn, cursor, username):
    ad = input(f"Hi {username}, don't you know where to go for the next holidays?\nType yes to have some advice! (yes) ")
    advice_data = []

    if ad.lower() == "yes":
        print(f"Welcome to the advice app, {username}!")
        print("Please enter your preferences:")
        continent = get_continent_for_advice()

        try:
            # Connect to the database
            countries = get_countries_per_continent(cursor, continent)
            if not countries:
                print("No countries found for the selected continent.")
                return advice_data

            country = get_country_for_advice(countries)
            weather = get_weather_for_advice()
            geography = get_geography_for_advice()

            offset = 0  # Initialize offset to 0 outside the loop
            num_cities = 5  # Set the default number of cities to 5

            # Fetch the initial set of recommendations from the database with a default of 5 cities
            suggestion = get_city_per_geography_and_weather_in_country(cursor, geography, weather, country, offset, num_cities)

            if len(suggestion) < 1:
                return print("Sorry, we couldn't find a city that aligns with your preferences. Please try using different features!")

            # Print the initial set of recommended cities
            for city in suggestion:
                print(city)
                advice_data.append(city)
            
            if len(suggestion) == 5:

                other = input("Do you want other recommended cities? (yes/no) ")

                while other.lower() == "yes":
                    offset += num_cities  # Update the offset for the next set of recommendations
                    num_cities = int(input("Enter the number of recommended cities you want to have: "))

                    # Fetch a new set of recommendations from the database
                    suggestion = get_city_per_geography_and_weather_in_country(cursor, geography, weather, country, offset, num_cities)

                    # Print the recommended cities
                    for city in suggestion:
                        print(city)
                        advice_data.append(city)

                    other = input("Do you want other recommended cities? (yes/no) ")

                    # Check if there are more cities to recommend
                    if not suggestion or len(suggestion) < num_cities:
                        print("No more cities to recommend.")
                        break

                print("Well, then have a nice trip!")
            
            else:
                print("We have no more cities to recommend, hope we've been useful!\nHave a nice trip!")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    return advice_data

# Just a little modification in order to have no limitations that is useful on our client-side
def get_city_per_geography_and_weather_in_country_no_stop(cursor, geography, weather, country): 
    try:
        cursor.execute('''
            SELECT DISTINCT city 
            FROM cities 
            WHERE Geography = ? AND Weather = ? AND Country = ?
        ''', (geography, weather, country))
        mylist = cursor.fetchall()
        result = [city[0] for city in mylist]
        return result
    except sqlite3.Error as e:
        print("Error retrieving cities:", e)
        return None



# Test the code
if __name__ == "__main__":
    conn, cursor = get_db_connection()
    if conn and cursor:
        try:
            username, _ = get_user_credentials()
            advice_with_db(conn, cursor, username)
        finally:
            close_connection(conn)

