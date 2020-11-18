#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class route:
    def __init__(self, name=None):

        self.name = name
        
        if name == "Exmouth_to_La_Gomera":
            self.name_start = "Exmouth"
            self.name_finish = "La Gomera"
            self.ifile_kml = "routes/Exmouth_La_Gomera.kml"
            self.xtick_inc_1 = 5
            self.ytick_inc_1 = 5
            self.extent_1 = [-20, 2.5, 25, 52.5]
            self.lat_ext2 = 5.0
            self.lon_ext2 = 5.0
            self.coast_alpha = [0.7, 0.7]
        elif name == "land_route":
            self.name_start = "Exmouth"
            self.name_finish = "Africa"
            self.ifile_kml = "routes/land_crew.kml"
            self.xtick_inc_1 = 5
            self.ytick_inc_1 = 5
            self.extent_1 = [-20, 2.5, 25, 52.5]
            self.lat_ext2 = 5.0
            self.lon_ext2 = 5.0
            self.coast_alpha = [0.7, 0.7]
        elif name == "UK_Exeter-Stornoway-Exeter":
            self.name_start = "Topsham"
            self.name_finish = "Turf via Stornoway"
            self.ifile_kml="routes/UK_Exeter-Stornoway-Exeter.kml"
            self.extent_1 = [-10.5, 2.5, 48, 60.5]
            self.xtick_inc_1 = 5
            self.ytick_inc_1 = 5
            self.lat_ext2 = 3.0
            self.lon_ext2 = 3.0
            self.coast_alpha = [0.0, 0.7]
        elif name == "Hamburg_to_Copenhagen":
            self.name_start = "Hamburg"
            self.name_finish = "Copenhagen"
            self.ifile_kml="routes/Hamburg_to_Copenhagen_1250_km.kml"
            self.extent_1 = [6.5, 13.5, 52.5, 57.999]
            self.lat_ext2 = 3.0
            self.lon_ext2 = 3.0
            self.xtick_inc_1 = 2
            self.ytick_inc_1 = 2
            self.coast_alpha = [0.7, 0.7]
        else:
            self.name_start = "???"
            self.name_finish = "???"
            self.ifile_kml="???.kml"
            self.extent_1 = [None, None, None, None]
            self.lat_ext2 = None
            self.lon_ext2 = None
            self.xtick_inc_1 = None
            self.ytick_inc_1 = None
            self.coast_alpha = [None, None]
