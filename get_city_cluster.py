import csv
from h3 import h3
import requests
import random
import db
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import json

city = 'Lviv'
URL = 'https://nominatim.openstreetmap.org/search.php?q=' + city + '+Ukraine&polygon_geojson=1&format=json'
r = requests.get(url=URL)
data = r.json()

coords = data[0]["geojson"]["coordinates"]
for coord in coords[0]:
    coord[0], coord[1] = coord[1], coord[0]

geoJson = {'type': 'Polygon',
           'coordinates': coords}
polygons = list(h3.polyfill(geoJson, 7))
hexagons = []
for hexagon in polygons:
    borders = h3.h3_to_geo_boundary(hexagon)
    hexagons.append({'id': hexagon,
                     'borders': Polygon(tuple(borders))})
    dots = [item for sublist in borders for item in sublist]
    db.insert_cluster(hexagon, random.randint(0, 2 ** 16), dots, city)
