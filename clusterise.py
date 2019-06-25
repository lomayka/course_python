import db
from h3 import h3
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

clusters = db.fetch_all_clusters()
renewed = []

rides = db.fetch_all_rides()
j = 1
for cluster in clusters:
    borders = []
    for i in range(6):
        renewed = [cluster[3][i * 2], cluster[3][i * 2 + 1]]
        borders.append(renewed)
    polygon = Polygon(tuple(borders))
    print(j)
    j += 1
    for ride in rides:
        point_cortege = Point(tuple([ride[4], ride[3]]))
        if point_cortege.within(polygon):
            db.ride_to_cluster(cluster[0], ride[0])
