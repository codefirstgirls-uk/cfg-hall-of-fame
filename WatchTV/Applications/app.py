from flask import Flask, app
from Applications.route import home

app = Flask(__name__)

app.add_url_rule('/', view_func=home) #register routes


if __name__ == '__main__':
    app.run(debug=True)
