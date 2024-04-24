''' To see the project run this file '''

# app.py
from flask import Flask
from flask_login import LoginManager
from website.auth import auth
from website.trip_planner import trip_planner
from website.database.AdviceDB import get_db_connection, close_connection
from website import create_app

app = create_app()

# Register Blueprints
app.register_blueprint(trip_planner)

if __name__ == '__main__':
    conn,_ = get_db_connection()

    if conn:
        try:
            app.run(debug=True)
        finally:
            close_connection(conn)

    app.run(debug=True)
