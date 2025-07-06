"""
This script runs the FlaskWebProject application using a development server.
"""
from os import environ
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, ssl_context='adhoc')
