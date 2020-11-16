#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def travel(distance, lat_route, lon_route):
    import numpy as np
    from geopy import distance as geodis

    latlon = tuple(zip(lat_route, lon_route))
    s_vec = np.empty(len(lat_route))
    s_sum = np.empty(len(lat_route))
    s_vec[:] = np.NaN
    s_sum[:] = np.NaN
    for n in range(len(lat_route)):
        if n == 0:
            s_vec[n] = 0.0
            s_sum[n] = 0.0
        else:
            s_vec[n] = geodis.distance(latlon[n], latlon[n-1]).m
            s_sum[n] = s_vec[n] + s_sum[n-1]

    # Find position of boat and the remaining distance
    # traveled  beyond last resolved waypoint
    lat_pos = lat_route[0]
    lon_pos = lon_route[0]
    for n in range(len(s_sum)):
        if s_sum[n] > distance:
            lat_pos = lat_route[n-1]
            lon_pos = lon_route[n-1]
            res = distance - s_sum[n-1]
            break

    # ToDo: Correct position by travelling the distance res
    #       from the last know position (lat_pos, lon_pps)

    return lat_pos, lon_pos, s_sum[n-1], s_sum[-1], res


def vrt_eta(t1=None, t2=None, s1=None, s2=None, s3=None):
    "Estimate arrival time"

    import datetime as dt

    t12 = (t2-t1).total_seconds()
    v12 = (s2-s1) / t12

    # Assume to continue travel with average velocity
    v23 = v12
    t23 = (s3-s2)/v23

    t3 = t2 + dt.timedelta(seconds=t23)

    return t3
