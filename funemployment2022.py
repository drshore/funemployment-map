# import sqlite3
# from flask import Flask, render_template
# from werkzeug.exceptions import abort

# def get_db_connection():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# def get_legs_by_mode(mode_name):
#     conn = get_db_connection()
#     mode = conn.execute('SELECT * FROM posts WHERE mode = ?',
#                         (mode_name,)).fetchone()
#     conn.close()
#     if mode_name is None:
#         abort(404)
#     return mode

# app = Flask(__name__)


# @app.route('/')
# def map():    
#     mapbox_access_token = 'YOUR ACCESS TOKEN HERE'
#     conn = get_db_connection()
#     legs = conn.execute('SELECT * FROM legs').fetchall()
#     conn.close()
#     return render_template('funemployment2022_travelmap.html', legs=legs,
#         mapbox_access_token=mapbox_access_token)


# def mapbox_gl():
#     return render_template(
#         'mapbox_gl.html', 
#         ACCESS_KEY=MAPBOX_ACCESS_KEY
#     )


import json
import requests
from geojson import Point, Feature

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']

# ROUTE = [
#     {"lat":37.7773159, "long":-122.4789618, "name": "SF Home", "is_stop_location": True},
#     {"lat":47.689452, "long":-122.322404, "name": "Andy+Zoey Home", "is_stop_location": True},
#     {"lat":48.9242888, "long":-122.077093, "name": "Maple Falls, Washington", "is_stop_location": True},
#     {"lat":49.2827291, "long":-123.1207375, "name": "Vancouver, Canada", "is_stop_location": True},
#     {"lat":47.689452, "long":-122.322404, "name": "511 Northeast 84th Street, Seattle, WA 98115, USA", "is_stop_location": True},
#     {"lat":45.515232, "long":-122.6783853, "name": "Portland, Oregon", "is_stop_location": True},
#     {"lat":44.0581728, "long":-121.3153096, "name": "Bend, Oregon", "is_stop_location": True},
#     {"lat":43.6150186, "long":-116.2023137, "name": "Boise, Idaho", "is_stop_location": True},
#     {"lat":40.7607793, "long":-111.8910474, "name": "Salt Lake City, Utah", "is_stop_location": True},
#     {"lat":37.2982022, "long":-113.0263005, "name": "Zion National Park, Utah", "is_stop_location": True},
#     {"lat":37.5930377, "long":-112.1870895, "name": "Bryce Canyon National Park, Utah", "is_stop_location": True},
#     {"lat":38.0877312, "long":-111.1354983, "name": "Capitol Reef National Park, Utah", "is_stop_location": True},
#     {"lat":38.2135733, "long":-109.9025345, "name": "Canyonlands National Park, Utah", "is_stop_location": True},
#     {"lat":38.733081, "long":-109.5925139, "name": "Arches National Park, Utah", "is_stop_location": True},
#     {"lat":39.5505376, "long":-107.3247762, "name": "Glenwood Springs, Colorado", "is_stop_location": True},
#     {"lat":41.8666341, "long":-103.6671662, "name": "Scottsbluff, Nebraska", "is_stop_location": True},
#     {"lat":43.5724388, "long":-103.4415644, "name": "Wind Cave National Park, SD", "is_stop_location": True},
#     {"lat":43.8553804, "long":-102.3396912, "name": "Badlands National Park, SD", "is_stop_location": True},
#     {"lat":46.8771863, "long":-96.7898034, "name": "Fargo, North Dakota", "is_stop_location": True},
#     {"lat":44.977753, "long":-93.2650108, "name": "Minneapolis, MN", "is_stop_location": True},
#     {"lat":43.3033056, "long":-91.7857092, "name": "Decorah, Iowa", "is_stop_location": True},
#     {"lat":43.0721661, "long":-89.4007501, "name": "Madison, WI", "is_stop_location": True},
#     {"lat":43.0389025, "long":-87.9064736, "name": "Milwaukee, WI", "is_stop_location": True},
#     {"lat":41.8781136, "long":-87.6297982, "name": "Chicago, Illinois", "is_stop_location": True},
#     {"lat":41.6532678, "long":-87.0524338, "name": "Indiana Dunes National Park, Indiana", "is_stop_location": True},
#     {"lat":39.768403, "long":-86.158068, "name": "Indianapolis, Indiana", "is_stop_location": True},
#     {"lat":37.3826741, "long":-80.1097462, "name": "Catawba, Virginia", "is_stop_location": True},
#     {"lat":37.5407246, "long":-77.4360481, "name": "Richmond, VA", "is_stop_location": True},
#     {"lat":41.5034271, "long":-74.0104178, "name": "Newburgh, NY", "is_stop_location": True},
#     {"lat":44.4758825, "long":-73.212072, "name": "Burlington, VT", "is_stop_location": True},
#     {"lat":44.3879504, "long":-71.1727881, "name": "Gorham, NH", "is_stop_location": True},
#     {"lat":44.3385559, "long":-68.2733346, "name": "Acadia National Park, Maine", "is_stop_location": True},
#     {"lat":42.3600825, "long":-71.0588801, "name": "Boston, MA", "is_stop_location": True},
#     {"lat":39.7876112, "long":-75.6966001, "name": "Hockessin, DE", "is_stop_location": True},
#     {"lat":39.744655, "long":-75.5483909, "name": "Wilmington, DE", "is_stop_location": True},
#     {"lat":39.9525839, "long":-75.1652215, "name": "Philadelphia, PA", "is_stop_location": True},
#     {"lat":39.0839973, "long":-77.1527578, "name": "Rockville, MD", "is_stop_location": True},
#     {"lat":37.5407246, "long":-77.4360481, "name": "Richmond, VA", "is_stop_location": True},
#     {"lat":38.851242, "long":-77.0402315, "name": "Reagan International Airport", "is_stop_location": True}
# ]

# # Mapbox driving direction API call
# ROUTE_URL = "https://api.mapbox.com/directions/v5/mapbox/driving/{0}.json?access_token={1}&overview=full&geometries=geojson"

# def create_route_url(route_batch):
#     # Create a string with all the geo coordinates
#     lat_longs = ";".join(["{0},{1}".format(point["long"], point["lat"]) for point in route_batch])
#     # Create a url with the geo coordinates and access token
#     url = ROUTE_URL.format(lat_longs, MAPBOX_ACCESS_KEY)
#     return url

# def create_stop_location_detail(title, latitude, longitude, index, route_index):
#     point = Point([longitude, latitude])
#     properties = {
#         "title": title,
#         'marker-color': '#3bb2d0',
#         'marker-symbol': index,
#         'route_index': route_index
#     }
#     feature = Feature(geometry = point, properties = properties)
#     return feature

# def create_stop_locations_details():
#     stop_locations = []
#     for route_index, location in enumerate(ROUTE):
#         if not location["is_stop_location"]:
#             continue
#         stop_location = create_stop_location_detail(
#             location['name'],
#             location['lat'],
#             location['long'],
#             len(stop_locations) + 1,
#             route_index
#         )
#         stop_locations.append(stop_location)
#     return stop_locations
    
# def batch(iterable, n=1):
#     l = len(iterable)
#     for ndx in range(0, l, n):
#         yield iterable[ndx:min(ndx + n, l)]

# def get_route_data():
#     waypoints = []
#     geometry_full = {'coordinates':[], 'type': 'LineString'}
#     for x in batch(ROUTE, 25):
#     # Get the route url
#         route_url = create_route_url(x)
#     # Perform a GET request to the route API
#         result = requests.get(route_url)
#     # Convert the return value to JSON
#         data = result.json()
#         geometry_full['coordinates'] = geometry_full['coordinates'] + data["routes"][0]["geometry"]['coordinates']
#         waypoints = waypoints + data["waypoints"]
#     route_data = Feature(geometry = geometry_full, properties = {})
#     return route_data, waypoints

@app.route('/')
# def mapbox_gl():
#     route_data, waypoints = get_route_data()

#     stop_locations = create_stop_locations_details()

#     # For each stop location, add the waypoint index 
#     # that we got from the route data
#     for stop_location in stop_locations:
#         waypoint_index = stop_location.properties["route_index"]
#         waypoint = waypoints[waypoint_index]
#         stop_location.properties["location_index"] = route_data['geometry']['coordinates'].index(waypoint["location"])

#     return render_template('mapbox_gl.html',
#         ACCESS_KEY=MAPBOX_ACCESS_KEY,
#         route_data = route_data,
#         stop_locations = stop_locations
#     )


# @app.route('/funemployment2022')
def map():    
    return render_template('funemployment2022_travelmap.html',
        ACCESS_KEY=MAPBOX_ACCESS_KEY)