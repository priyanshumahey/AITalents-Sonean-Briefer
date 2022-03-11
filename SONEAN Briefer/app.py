from flask import Flask, url_for, render_template, request, redirect
from flask.json import jsonify
import pandas as pd
import numpy as np
import json
import csv
import logging


#Reading the map data
log = logging.getLogger(__name__)

def get_data():
    data = {}
    with open('src/resources/data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data['categories'] = {
            i: category for i, category in enumerate(next(reader)[1:])
        }
        data['countries'] = {}
        for i, row in enumerate(reader):
            try:
                country = row[0]
                data['countries'][country] = {
                    category: validate_value(value)
                    for category, value in enumerate(row[1:])
                }
            except (ValueError, TypeError):
                log.debug('Problem with line %d: ', i, exc_info=True)

    return data

def validate_value(value):
    try:
        return float(value)
    except ValueError:
        return ''



#Data for the table
gsheet = ""
gsheet = ""

sheet_name = "Claas"
gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheet, sheet_name)
 
df = pd.read_csv(gsheet_url)
print(df)
dicta = df.to_dict('index')

table_data = []
for i in range(len(dicta)):
    table_data.append(dicta[i])
print(table_data[1])

table_columns = [{
        "field": "Date",
        "title": "Date",
        "sortable" : True,
    },
    {
        "field": "Source Tag",
        "title": "Source Tag",
        "sortable" : True,
    },
    {
        "field": "Country",
        "title": "Country",
        "sortable" : True,
    },
    {
        "field": "Organization",
        "title": "Organization",
        "sortable" : True,
    },
    {
        "field": "Host",
        "title": "Host",
        "sortable" : True,
    },
    {
        "field": "Name",
        "title": "Name",
        "sortable" : True,
    },
    {
        "field": "Factor",
        "title": "Factor",
        "sortable" : True,
    },
    {
        "field": "Content",
        "title": "Content",
        "sortable" : True,
    }]


##List of passwords and usernames
username_list = ['User']
password_list = ['Pass']


##Flask stuff
app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def homepage():
    return render_template('homepage.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] not in username_list or request.form['password'] not in password_list:
            error = 'Incorrect password or username.'
        else:
            return redirect(url_for('.dashboard_home'))
    return render_template('login.html', error=error)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        newuser = request.form["username"]
        newpass = request.form['password']
        username_list.append(newuser)
        password_list.append(newpass)
        return redirect(url_for('.login'))
    return render_template('register.html')


@app.route("/dashboardhome", methods=["POST", "GET"])
def dashboard_home():
    return render_template('dashboard_home.html')


@app.route("/table")
def index():
    return render_template("main_dashboard.html", data =table_data, columns=table_columns, title='Dashboard' )


@app.route('/api/v1/data', methods=['GET'])
def data():
    return jsonify(get_data())

@app.route('/api/v1/categories', methods=['GET'])
def categories():
    return jsonify([
        {'id': key, 'name': name}
        for key, name in get_data()['categories'].items()
    ])


@app.route('/api/v1/category/<int:category>', methods=['GET'])
def category_data(category):
    return jsonify([
        (country, values[category])
        for country, values in get_data()['countries'].items()
        if values[category]
    ])


@app.route('/dashboardhome/briefing', methods=['POST', 'GET'])
def briefing():
    return render_template('briefing.html')

if __name__ == "__main__":
    app.run(debug=True)
