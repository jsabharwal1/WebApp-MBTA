from flask import Flask, render_template, request
from mbta_helper import find_stop_near, get_weather, get_nearest_station, get_lat_long


app = Flask(__name__)

#@app.route('/')

@app.get('/station/')
def station_get():
    return render_template("index.html", error=None)

@app.post('/station/')
def station_post():
    place_name = str(request.form["place_name"])
    route_type = str(request.form["route_type"])
    station, wheelchair_accessible = find_stop_near(place_name, route_type)
    weather, temperature = get_weather(place_name)

    if wheelchair_accessible == 0:
        wheelchair = 'No Information'
    elif wheelchair_accessible == 1:
        wheelchair = 'Accessible'
    else:
        wheelchair = 'Inaccessible'   
    if station:
        return render_template('result.html', place=place_name, station=station, wheelchair=wheelchair, route=route_type, weather = weather, temperature=temperature)
    else:
        return render_template('index.html', error=True)



@app.route('/')
def result():

    return render_template('index.html', station=station_get, post=station_post)
    

if __name__ == '__main__':
    app.run(debug=True)
