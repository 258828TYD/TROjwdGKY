"""
This script runs the FlaskWebProject application using a development server.
"""
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
    except ValueError:
    app.run(HOST, PORT, ssl_context='adhoc')
