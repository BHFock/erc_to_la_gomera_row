#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():

    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cf
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    import datetime as dt
    import sys
    import math
    import numpy as np
    import iris
    import iris.plot as iplt

    sys.path.append(sys.path[0] + "/src")

    from src import kml2latlon
    from src import read_logbook
    from src import travel
    from src import vrt_eta
    from src import team
    from src import route

    # User input

    start_date = dt.datetime(2020,10,31)
    logbook = "log/rowing.log"

    # ToDo allow team specific routes
    #r=route(name="Hamburg_to_Copenhagen")
    #r=route(name="UK_Exeter-Stornoway-Exeter")
    r=route(name="Exmouth_to_La_Gomera")

    # Uncomment 1-2 teams to select plotted crew
    crews = []
    crews.append(team(config_file="rowing.conf"))
    crews.append(team(config_file="land_crew.conf"))

    # Read and calculate data
    for crew in crews:
        final_date = dt.date.today().strftime("%Y-%m-%d")
        date_2 = dt.datetime.strptime(final_date,'%Y-%m-%d') - dt.timedelta(days=1)
        d2 = dt.date.today()

        # ToDo rewrite the functions as methods accoiated with the team class ?
        crew.lat_route, crew.lon_route = kml2latlon(r.ifile_kml)
        crew.s, crew.date_last_log = read_logbook("log/" + crew.logbook)
        crew.lat, crew.lon, crew.sw, crew.s_end, crew.res = travel(crew.s, crew.lat_route, crew.lon_route)
        crew.sdm1, _ = read_logbook("log/" + crew.logbook, d1=date_2.strftime('%Y-%m-%d'), d2=final_date)
        crew.eta = vrt_eta(t1=start_date, t2=crew.date_last_log, s1=0.0, s2=crew.s, s3=crew.s_end)

    # Plot data

    xticks_1 = range(-180,180,r.xtick_inc_1)
    yticks_1 = range(0,90,r.ytick_inc_1)

    extent_2 = np.empty(shape=(len(crews),4))
    for i in range(len(crews)):
        extent_2[i,:] = [math.floor(crews[i].lon)-0.5*r.lon_ext2,
                         math.floor(crews[i].lon)+0.5*r.lon_ext2,
                         math.floor(crews[i].lat)-0.5*r.lat_ext2,
                         math.floor(crews[i].lat)+0.5*r.lat_ext2]

    xticks_2 = range(-180,180,1)
    yticks_2 = range(-90,90,1)

    proj = ccrs.PlateCarree()

    fig = plt.figure(figsize=(16, 9))

    fig.suptitle(r.name_start + ' to ' + r.name_finish
                 + ' ({:.0f} km)'.format(crews[0].s_end/1000.0) + ' \n'
                 + start_date.strftime("%Y-%m-%d") + ' - '
                 + crews[0].date_last_log.strftime("%Y-%m-%d") )

    land_10m = cf.NaturalEarthFeature('physical', 'land', '10m',
                                      edgecolor='face', facecolor=cf.COLORS['land'])

    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()

    ax1 = fig.add_subplot(1, 2, 1, projection=proj)

    ax1.add_feature(land_10m)
    ax1.coastlines(resolution='10m', color='gray', alpha=r.coast_alpha[0])
    ax1.set_xticks(xticks_1)
    ax1.set_yticks(yticks_1)
    ax1.set_extent(r.extent_1, crs=proj)
    ax1.xaxis.set_major_formatter(lon_formatter)
    ax1.yaxis.set_major_formatter(lat_formatter)

    ax1.plot(crews[0].lon_route[0], crews[0].lat_route[0], marker='o', color='grey', markersize=6, alpha=1.0, transform=proj)
    ax1.plot(crews[0].lon_route[-1], crews[0].lat_route[-1], marker='o', color='grey', markersize=5, alpha=0.7, transform=proj)

    ax1.plot(crews[0].lon_route, crews[0].lat_route, ':', linewidth=2, color='blue', transform=proj)

    ax = [None] * len(crews)
    i=0
    for crew in crews:
        ax[i] = fig.add_subplot(1, 2, 1, projection=proj)
        ax[i].plot(crew.lon, crew.lat, marker='o', color=crew.color,
                   markersize=8, alpha=0.7, transform=proj)
        i=i+1

    ax1.set_title('Distance from ' + r.name_start + ': '
                  + '{:.0f} km \n'.format((crews[0].s)/1000.)
                  + 'Estimated time of arrival: '
                  + crews[0].eta.strftime('%a %d %b %Y %H:%M'))

    ax2 = fig.add_subplot(0+len(crews), 2, 2, projection=proj)
    ax2.add_feature(land_10m)
    ax2.coastlines(resolution='10m',color='gray', alpha=r.coast_alpha[1])
    ax2.set_xticks(xticks_2)
    ax2.set_yticks(yticks_2)
    ax2.set_extent(extent_2[0,:])
    ax2.xaxis.set_major_formatter(lon_formatter)
    ax2.yaxis.set_major_formatter(lat_formatter)
    ax2.plot(crews[0].lon_route[0], crews[0].lat_route[0], marker='o', color='blue', markersize=4, alpha=0.7, transform=proj)
    ax2.plot(crews[0].lon_route[-1], crews[0].lat_route[-1], marker='o', color='blue', markersize=4, alpha=0.7, transform=proj)
    ax2.plot(crews[0].lon_route, crews[0].lat_route, ':', transform=proj)
    ax2.plot(crews[0].lon, crews[0].lat, marker='o', color='red', markersize=8, alpha=0.7, transform=proj)
    ax2.set_title('Distance ' + d2.strftime("%a %d %b %Y") + ": " + '{:.0f} km'.format(crews[0].sdm1/1000.))

    i=1
    if (len(crews)==2):
        ax3 = fig.add_subplot(0+len(crews), 2, 2+len(crews), projection=proj)
        ax3.add_feature(land_10m)
        ax3.coastlines(resolution='10m',color='gray', alpha=r.coast_alpha[1])
        ax3.set_xticks(xticks_2)
        ax3.set_yticks(yticks_2)
        ax3.set_extent(extent_2[i,:])
        ax3.xaxis.set_major_formatter(lon_formatter)
        ax3.yaxis.set_major_formatter(lat_formatter)
        ax3.plot(crews[i].lon_route[0], crews[i].lat_route[0], marker='o', color='blue', markersize=4, alpha=0.7, transform=proj)
        ax3.plot(crews[i].lon_route[-1], crews[i].lat_route[-1], marker='o', color='blue', markersize=4, alpha=0.7, transform=proj)
        ax3.plot(crews[i].lon_route, crews[i].lat_route, ':', transform=proj)
        ax3.plot(crews[i].lon, crews[i].lat, marker='o', color=crews[i].color, markersize=8, alpha=0.7, transform=proj)
        ax3.set_title('Distance ' + d2.strftime("%a %d %b %Y") + ": " + '{:.0f} km'.format(crews[i].sdm1/1000.))

    # plt.show()
    plt.savefig("plots/Exmouth_RC_virtual_row_winter_2020--2021.png")


if __name__ == "__main__":
    main()
