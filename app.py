from flask import Flask, render_template, request
import os, requests, json, time
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
db = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    def AddCityInDataBase(AddInDataBase):
        Query = "INSERT INTO CityNames (No, Name) VALUES (%s, %s)"
        City = (' ', Temporary)
        cursor = db.connection.cursor()
        cursor.execute(Query, City)
        db.connection.commit()
    
    if request.method == 'POST': 
        AddCity = request.form['city']
        Temporary = str(AddCity)
        AddCityInDataBase(Temporary)
        
    Query = "SELECT * from CityNames"
    cursor = db.connection.cursor()
    cursor.execute(Query)
    WeatherData = []
    API_KEY = os.getenv('APIKEY')
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid='+API_KEY
    print(url)
    for NewCity in cursor:
        NewCity = str(NewCity[1])
        result = requests.get(url.format(NewCity)).json()
        Temp = int(result['main']['temp']) - 273
        CityName = result['weather'][0]['description']
        CityName = CityName.capitalize()
        weather = {
            'city': result['name'],
            'temp': Temp,
            'description': CityName,
            'icon': result['weather'][0]['icon']
        }
        WeatherData.append(weather)
    return render_template('index.html', WeatherData=WeatherData)

if __name__ == "__main__":
    app.run(debug=True)