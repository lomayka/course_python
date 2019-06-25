import random

import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
import numpy
import scipy
# #from statsmodels.tsa.arima_model import ARIMA
# import json
# import ntpath

import db


def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return numpy.array(diff)


def inverse_difference(history, yhat, interval=1):
    return yhat + history[-interval]


clusters = db.clusters_by_city("Lviv")
a = 1
for cluster in clusters:
    print(cluster[0])
    rides = db.rides_by_cluster(cluster[0])
    dates = {}
    for ride in rides:
        ddate = pd.to_datetime(ride[0]).replace(microsecond=0, second=0, minute=0)
        if ddate in dates:
            dates[ddate] += 1
        else:
            dates[ddate] = 1

    data_set = pd.DataFrame.from_dict(dates, orient="index")
    data_set.plot(figsize=(20, 10))
    series = data_set
    # seasonal difference
    X = series.values

    try:
        days_in_year = 365
        differenced = difference(X, days_in_year)
        # fit model
        model = ARIMA(differenced, order=(7, 0, 1))
        model_fit = model.fit(disp=0)
        # multi-step out-of-sample forecast
        start_index = len(differenced)
        end_index = start_index + 168
        forecast = model_fit.predict(start=start_index, end=end_index)
        # invert the differenced forecast to something usable
        history = [x for x in X]
        day = 1
        for yhat in forecast:
            inverted = inverse_difference(history, yhat, days_in_year)
            print(day, inverted[0], a)
            db.weight_to_cluster(day, inverted[0], cluster[0])
            history.append(inverted)
            day += 1

    except Exception as e:
        print(e)
        for i in range(1, 169):
            print(i, -1, a)
            db.weight_to_cluster(i, -1, cluster[0])
    a += 1
