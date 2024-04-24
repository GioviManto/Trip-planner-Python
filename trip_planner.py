
from website.auth import auth  
from flask import Flask,Blueprint,render_template, request, request, session, jsonify, g
from flask_login import LoginManager,login_user, login_required, logout_user, current_user
from website.database.AdviceDB import connect_to_database, get_db_connection, close_connection, get_countries_per_continent, get_city_per_geography_and_weather_in_country_no_stop
import sqlite3
from web_automation import days_difference, flights, activities, hotels
from website.models import User


trip_planner = Blueprint('trip_planner', __name__)

@trip_planner.before_request
def before_request():
    print("Before request")
    g.db, g.cursor = get_db_connection()

@trip_planner.teardown_request
def teardown_request(exception):
    print("Teardown request")
    close_connection(g.db)

@trip_planner.route('/home', methods=['GET','POST'])
def home():
    return render_template("home.html")



@trip_planner.route('/trip-planner-yes', methods=['GET','POST'])
def trip_planner_yes():
    return render_template('trip_planner_yes.html', user=current_user)

@trip_planner.route('/day-calc', methods=['GET','POST'])
def handle_date():
    try:
        start_date = request.form.get('startDate')
        end_date = request.form.get('endDate')
        destination = request.form.get('destination')
        budget_flight = request.form.get('budgetFlight')
        budget_hotel = request.form.get('budgetHotel')
        number_guests = request.form.get('numberGuest')
        Origin = request.form.get('Origin')

        
        # Fai qualcosa con start_date, ad esempio salvarlo nella sessione
        session['start_date'] = start_date
        session['end_date'] = end_date
        session['destination'] = destination
        session['Origin'] = Origin
        session['budget_flight'] = budget_flight
        session['budget_hotel'] = budget_hotel
        session['number_guests'] = number_guests
        print('Received startDate:', start_date)
        print('Received endDate:', end_date)
        print('Received Origin:', Origin)
        print('Received destination:', destination)
        print('Received budgetFlight:', budget_flight)
        print('Received budgetHotel:',budget_hotel )
        print('Received numberGuest:', number_guests)

        
        
        # Calculate the difference between start and end dates
        diff = days_difference(end_date, start_date)
        print(diff)
        hotel_results = hotels(budget_hotel, number_guests, start_date, end_date, destination, diff)
        print(hotel_results)
        activ=activities(destination,diff)
        print(activ)
        flight_results= flights(start_date, end_date, destination, Origin, budget_flight, number_guests)
        print(flight_results)
        
        return jsonify({
            'success': True,
            'difference': diff,
            'hotel_results': hotel_results,
            'activities': activ,
            'flight_results': flight_results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

        
   

@trip_planner.route('/trip-planner-no')
def trip_planner_no():
    print("Inside trip_planner_no route")
    username = current_user.first_name
    print('Username: ', username)
    return render_template('trip_planner_no.html', username=username)


@trip_planner.route('/advice')
def advice():
    return render_template('advice.html', username=current_user.first_name)

@trip_planner.route('/advice-data', methods=['GET', 'POST'])
def advice_process():
    try:
        # Get the request data
        selected_continent = request.form.get('continent')
        selected_country = request.form.get('country')
        selected_weather = request.form.get('weather')
        selected_geography = request.form.get('geography')

        # Store the data in the session
        session['selected_continent'] = selected_continent
        session['selected_country'] = selected_country
        session['selected_weather'] = selected_weather
        session['selected_geography'] = selected_geography

        print(session['selected_continent'])
        print(session['selected_country'])
        print(session['selected_weather'])
        print(session['selected_geography'])

        # Function 1: Handle continent selection
        def handle_continent(cursor):
            countries = get_countries_per_continent(cursor, selected_continent)
            return jsonify({'countries': countries})

        # Call the appropriate function based on the received data
        if selected_continent:
            countries = handle_continent(g.cursor)
            return countries

        if selected_country and selected_weather and selected_geography:
            recommended_cities = get_city_per_geography_and_weather_in_country_no_stop(g.cursor, selected_geography, selected_weather, selected_country)
            # Close the database connection
            close_connection(g.db)
            response_data = {'cities': recommended_cities, 'message': 'Success'}
            return jsonify(response_data)
        else:
            close_connection(g.db)
            return jsonify({'message': 'No data provided for advice'})
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred during advice processing'})


@trip_planner.route('/advice-results', methods=['GET', 'POST'])
def advice_results():
    # Get the selected data from the session
    selected_continent = session.get('selected_continent')
    selected_country = session.get('selected_country')
    selected_weather = session.get('selected_weather')
    selected_geography = session.get('selected_geography')

    print(selected_continent)
    print(selected_country)
    print(selected_weather)
    print(selected_geography)

    # Check if all required data is available
    if selected_continent and selected_country and selected_weather and selected_geography:
        # Process the data and get the recommended cities 
        recommended_cities = get_city_per_geography_and_weather_in_country_no_stop(
            g.cursor,  
            selected_geography,
            selected_weather,
            selected_country
        )
        q = 0
        if recommended_cities:
            for city in recommended_cities:
                q += 1
                print(city)
        else:
            print('There is no city')
        
        print("The number of recommended cities is ", q)

        # Close the database connection
        close_connection(g.db)

        # Return a JSON response
        response_data = {'cities': recommended_cities, 'message': 'Success'}
        return render_template('advice_results.html', **response_data, username = current_user.first_name)

    else:
        # Handle the case when no specific data is available
        close_connection(g.db)
        return render_template('advice_results.html', message='No data provided for advice')
    

@trip_planner.route('/load-more-cities', methods=['POST'])
def load_more_cities():
    try:
        # Get the selected data from the session
        selected_continent = session.get('selected_continent')
        selected_country = session.get('selected_country')
        selected_weather = session.get('selected_weather')
        selected_geography = session.get('selected_geography')


        # Check if all required data is available
        if selected_continent and selected_country and selected_weather and selected_geography:
            # Process the data and get the next set of recommended cities (
            recommended_cities = get_city_per_geography_and_weather_in_country_no_stop(
                g.cursor,
                selected_geography,
                selected_weather,
                selected_country
            )

            # Get the index from the request data
            index = int(request.form.get('index', 0))

            # Return the next 5 cities starting from the current index
            response_data = {'cities': recommended_cities[index:index + 5], 'message': 'Success'}
            close_connection(g.db)
            return jsonify(response_data)
        else:
            # Handle the case when no specific data is available
            close_connection(g.db)
            return jsonify({'message': 'No data provided for advice'})
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred during advice processing'})


