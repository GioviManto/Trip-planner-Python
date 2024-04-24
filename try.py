'''This file is just to see if the most important functions are actually working the way they should'''

from AdviceDB import connect_to_database, close_connection, get_continent_for_advice, get_countries_per_continent, get_country_for_advice, get_city_per_country_in_continent, get_weather_for_advice, get_city_per_weather_in_country, get_geography_for_advice, get_city_per_geography_in_country, get_db_connection
import sqlite3

def get_city_per_geography_and_weather_in_country(cursor, geography, weather, country): 
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



if __name__ == "__main__":
    conn, cursor = get_db_connection()
    if conn and cursor:
        try:
            sel_continent = get_continent_for_advice()
            print("Selected continent" + sel_continent)

            countries = get_countries_per_continent(cursor,sel_continent)

            sel_country = get_country_for_advice(countries)
            cities_in_country = get_city_per_country_in_continent(cursor,sel_country)
            print("Cities in the selected country: ")
            for city in cities_in_country:
                print(city)

            sel_weather = get_weather_for_advice()
            cities_in_country_per_weather = get_city_per_weather_in_country(cursor,sel_weather,sel_country)
            print("Cities in the country per" + sel_weather + "weather: ")
            for city in cities_in_country_per_weather:
                print(city)
                
            sel_geography = get_geography_for_advice()
            cities_in_country_per_geography = get_city_per_geography_in_country(cursor,sel_geography,sel_country)
            print("Cities in the country per" + sel_geography + "geography: ")
            for city in cities_in_country_per_geography:
                print(city)
            
            cities_in_country_per_geography_and_weather = get_city_per_geography_and_weather_in_country(cursor,sel_geography,sel_weather,sel_country)
            print("Cities in the country per geography and weather: ")
            for city in cities_in_country_per_geography_and_weather:
                print(city)


            output_set = set(cities_in_country_per_weather) & set(cities_in_country_per_geography)
            output = list(output_set)
            print("Cities in the country per geography and weather in the output list: ")
            for city in output:
                print(city)

            if len(output) == len(cities_in_country_per_geography_and_weather):
                print("OK")
            else:
                print("Mismatch between output length and expected length.")

                
        finally:
            close_connection(conn)