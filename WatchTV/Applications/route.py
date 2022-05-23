# routes for all files.
from flask import render_template


def home():
    return render_template('home.html', title='Home')

# @app.route('/home')
# @app.route("/")
# def home():
#     return render_template('home.html')
