import os
import pandas as pd
import requests
import json
import settings

MAPBOX_ACCESS_KEY = os.environ.get('MAPBOX_ACCESS_KEY')

def create_route_json(row):
    """Get route JSON."""
    coordinate_list = []
    if row['mode'] in ('driving', 'cycling', 'hiking'):
        base_url = 'https://api.mapbox.com/directions/v5/mapbox/'
        if row['mode'] in ('driving', 'bus'):
            route_type = 'driving/'
        if row['mode'] == 'cycling':
            route_type = 'cycling/'
        if row['mode'] == 'hiking':
            route_type = 'walking/'
        url = base_url + route_type + str(row['origin_longitude']) + \
            ',' + str(row['origin_latitude']) + \
            ';' + str(row['destination_longitude']) + \
            ',' + str(row['destination_latitude'])
        params = {
            'geometries': 'geojson',
            'access_token': mapbox_api_token
        }
        req = requests.get(url, params=params)
        # print(row['start > end'])
        # print(req.json())
        route_json = req.json()['routes'][0]
        for i in route_json['geometry']['coordinates']:
            coordinate_list.append(i)
    if row['mode'] in ('flight', 'train', 'ferry'):
        coordinate_list.append([row['origin_latitude'], row['origin_longitude']])
        coordinate_list.append([row['destination_latitude'], row['destination_longitude']])
    return coordinate_list
    # create_route_geojson(route_json, row['start > end'])


routes_df['directions_coordinates'] = routes_df.apply(create_route_json, axis=1)
routes_df.to_csv('legs_with_direction_coordinates.csv')