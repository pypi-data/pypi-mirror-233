from flask import Flask
# This is an optional python file that let you also run the flask app online with a domain if you have a server host.

app = Flask('__name__') # Creates a flask app.

@app.route('/') # Returns the message once it's online.
def home():
    return 'Server is up and running!'

if __name__ == '__main__': # Entry point to run.
    app.run()