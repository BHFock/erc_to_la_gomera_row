#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def kml2latlon(ifile):
    """Read lon lat from kml file with single path"""
    from fastkml import kml, geometry

    with open(ifile, 'rt') as myfile:
        doc = myfile.read()
    k = kml.KML()
    k.from_string(doc.encode("utf-8"))
    f = list(k.features())
    g = list(f[0].features())[0].geometry

    lat = []
    lon = []
    for c in g.coords:
        lon.append(c[0])
        lat.append(c[1])

    return lat, lon
