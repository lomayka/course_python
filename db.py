import psycopg2

connect_read = psycopg2.connect("host=localhost dbname=course user=postgres password=123")
connect_write = psycopg2.connect("host=localhost dbname=course user=postgres password=123")

cursor_read = connect_read.cursor()
cursor_write = connect_write.cursor()


def ride_to_cluster(cluster_id, ride_id):
    insert = "INSERT INTO cluster_to_ride (ride_id, cluster_id) VALUES (%s, %s)"
    cursor_write.execute(insert, (ride_id, cluster_id))
    connect_write.commit()


def fetch_all_clusters():
    cursor_read.execute('SELECT * FROM clusters')
    return cursor_read.fetchall()


def fetch_all_rides():
    cursor_read.execute('SELECT * FROM rides')
    return cursor_read.fetchall()


def insert_cluster(id, city, dots):
    insert = "INSERT INTO clusters (id, city, dots) VALUES (%s, %s, %s)"

    cursor_write.execute(insert, (id, city, dots))
    connect_write.commit()


def clusters_by_city(city):
    sql = "SELECT * FROM clusters WHERE city = %s"
    c = (city,)
    cursor_read.execute(sql, c)
    return cursor_read.fetchall()


def rides_by_cluster(cluster_id):
    sql = """SELECT rides.created_at FROM rides
                INNER JOIN cluster_to_ride
                ON rides.ride_id = cluster_to_ride.ride_id WHERE cluster_to_ride.cluster_id = %s"""
    id = (cluster_id,)
    cursor_read.execute(sql, id)
    return cursor_read.fetchall()


def weight_to_cluster(dateindex, weight, cluster_id):
    sql = "INSERT INTO clusters_to_weight (weight, cluster_id, date) VALUES (%s, %s, %s)"

    cursor_write.execute(sql, (weight, cluster_id, dateindex))
    connect_write.commit()


def get_weight_of_date(date):
    sql = "SELECT * FROM clusters_to_weight WHERE date = %s"
    cursor_read.execute(sql, (date,))
    return cursor_read.fetchall()
