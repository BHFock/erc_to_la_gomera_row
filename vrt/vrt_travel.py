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
    res = 0.0
    for n in range(len(s_sum)):
        if s_sum[n] > distance:
            lat_pos = lat_route[n-1]
            lon_pos = lon_route[n-1]
            res = distance - s_sum[n-1]
            break

    if  distance > s_sum[n]:
        lat_pos = lat_route[n]
        lon_pos = lon_route[n]
        res = 0

    # ToDo: Correct position by travelling the distance res
    #       from the last know position (lat_pos, lon_pps)

    return lat_pos, lon_pos, s_sum[n-1], s_sum[-1], res

