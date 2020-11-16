#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class team:
    def __init__(self, config_file=None, boat=None, color=None,
                 logbook=None, members=None, name=None):

        import configparser

        #config file
        self.conf=config_file

        # set default
        self.boat="1x"
        self.color="red"
        self.members="NN"
        self.name="NN"

        # default position Beach Pub Exmouth
        self.lat = 50.61699
        self.lon = -3.422901

        self.s = 0.0     # distance traveled so far
        self.sdm1 = 0.0  # distance traveled after date_2 # ToDo organise as vector for all days
        self.sw = 0.0    # distance traveled to last way point
        self.res = 0.0   # distance traveled beyond last way point
        self.s_end = 0.0 # distance from start to finish

        self.date_last_log = "1517-10-31" # Martin Luther posts his 95 Theses

        # read config file
        config = configparser.ConfigParser()
        config.read("conf/" + config_file)
        for key in config['team']:
            if key=='boat':
                self.boat = config['team'][key]
            if key=='color':
                self.color = config['team'][key]
            if key=='logbook':
                self.logbook = config['team'][key]
            if key=='members':
                self.members = config['team'][key]
            if key=='name':
                self.name = config['team'][key]

        # overwrite values from config file if specified
        if boat:
            self.boat = boat
        if color:
            self.color = color
        if logbook:
            self.logbook = logbook
        if members:
            self.members = members
        if name:
            self.name = name
