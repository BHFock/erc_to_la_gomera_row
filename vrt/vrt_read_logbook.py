#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def read_logbook(ifile, d1=None, d2=None):
    import pandas
    import datetime as dt

    df = pandas.read_csv(ifile, sep=' *; *', engine='python')
    pandas.to_datetime(df['date'])
    if d1 is not None and d2 is not None:
        df = df.loc[(df['date'] > d1) & (df['date'] <= d2)]

    if(df.empty):
        distance = 0
        last_date = d2
    else:
        distance = df['meter'].sum(axis=0)
        last_date = dt.datetime.strptime(df['date'].values[-1], '%Y-%m-%d')

    return distance, last_date
