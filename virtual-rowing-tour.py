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

    #r=route(name="Hamburg_to_Copenhagen")
    #r=route(name="UK_Exeter-Stornoway-Exeter")
    r=route(name="Exmouth_to_La_Gomera")

    crews = []
    crews.append(team(config_file="rowing.conf"))
    crews.append(team(config_file="land_crew.conf"))

    #for crew in crews:
    #    print(crew.name)
    #sys.exit()

    # Read and calculate data

    final_date = dt.date.today().strftime("%Y-%m-%d")
    date_2 = dt.datetime.strptime(final_date,'%Y-%m-%d') - dt.timedelta(days=1)
    d2 = dt.date.today()
    
    lat_route, lon_route = kml2latlon(r.ifile_kml)
    s2, last_date = read_logbook(logbook)
    lat_boat, lon_boat, s_nm1, s_end, res = travel(s2, lat_route, lon_route)
    s_dm1, _ = read_logbook(logbook, d1=date_2.strftime('%Y-%m-%d'), d2=final_date)
    eta = vrt_eta(t1=start_date, t2=last_date, s2=s2, s3=s_end)

    # Plot data
    
    xticks_1 = range(-180,180,r.xtick_inc_1)
    yticks_1 = range(0,90,r.ytick_inc_1)

    # ToDo: Test if this works for all possible lon/lat positions - possible not!
    extent_2 = [math.floor(lon_boat)-0.5*r.lon_ext2, math.floor(lon_boat)+0.5*r.lon_ext2,
                math.floor(lat_boat)-0.5*r.lat_ext2, math.floor(lat_boat)+0.5*r.lat_ext2]

    xticks_2 = range(-180,180,1)
    yticks_2 = range(-90,90,1)
    
    proj = ccrs.PlateCarree()

    fig = plt.figure(figsize=(16, 9))

    fig.suptitle(r.name_start + ' to ' + r.name_finish
                 + ' ({:.0f} km)'.format(s_end/1000.) + ' \n'
                 + start_date.strftime("%Y-%m-%d") + ' - '
                 + last_date.strftime("%Y-%m-%d") )

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

    ax1.plot(lon_route[0], lat_route[0], marker='o', color='blue',
              markersize=6, alpha=1.0, transform=proj)
    ax1.plot(lon_route[-1], lat_route[-1], marker='o', color='blue',
             markersize=5, alpha=0.7, transform=proj)
    ax1.plot(lon_route, lat_route, ':', linewidth=2, transform=proj)
    ax1.plot(lon_boat, lat_boat, marker='o', color='red',
             markersize=8, alpha=0.7, transform=proj)
    ax1.set_title('Distance from ' + r.name_start + ': '
                  + '{:.0f} km \n'.format((s_nm1+res)/1000.)
                  + 'Estimated time of arrival: '
                  + eta.strftime('%a %d %b %Y %H:%M'))

    ax2 = fig.add_subplot(1, 2, 2, projection=proj)

    ax2.add_feature(land_10m)
    ax2.coastlines(resolution='10m',color='gray', alpha=r.coast_alpha[1])
    ax2.set_xticks(xticks_2)
    ax2.set_yticks(yticks_2)
    ax2.set_extent(extent_2)
    ax2.xaxis.set_major_formatter(lon_formatter)
    ax2.yaxis.set_major_formatter(lat_formatter)

    ax2.plot(lon_route[0], lat_route[0], marker='o', color='blue',
             markersize=4, alpha=0.7, transform=proj)
    ax2.plot(lon_route[-1], lat_route[-1], marker='o', color='blue',
             markersize=4, alpha=0.7, transform=proj)
    ax2.plot(lon_route, lat_route, ':', transform=proj)
    ax2.plot(lon_boat, lat_boat, marker='o', color='red',
             markersize=8, alpha=0.7, transform=proj)

    ax2.set_title('Distance ' + d2.strftime("%a %d %b %Y") + ": " +
                  '{:.0f} km'.format(s_dm1/1000.))

    # plt.show()
    plt.savefig("plots/Exmouth_RC_virtual_row_winter_2020--2021.png")


if __name__ == "__main__":
    main()
