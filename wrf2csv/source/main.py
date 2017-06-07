#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
import netCDF4

#######################################
import lat_lon
import out_put
import wrf_var
#######################################

path1 = (sys.argv[1]) #WRF files
path2 = (sys.argv[2]) #Output path
lat = (sys.argv[3]) #
lon = (sys.argv[4])

a = 0
for wrf_file in os.listdir(path1):
	a += 1
print "########################################################\n\n"
print "Total fils: %i\n" % (a)
print "########################################################\n\n"
print "Running ...\n"	
for wrf_file in os.listdir(path1):
	WRFfile = netCDF4.Dataset(path1+wrf_file, 'r')
	ix, iy = lat_lon.WRF_grab(WRFfile, float(lat), float(lon))
	out_name, date0 = out_put._get_name_date(wrf_file)
	date_r, rain = wrf_var._get_rain(WRFfile, ix, iy,  date0, 0)
	date_t, temp_max, temp_min = wrf_var._get_temp(WRFfile, ix, iy,  date0, 0)
	eof = out_put._make_files(out_name, path2, rain, temp_min, temp_max, date_r)
	if eof == True:
		print "########################################################\n"
		print "%s is Done!\n" % (out_name)
		print "########################################################\n"
	else:
		print "########################################################\n"
		print "%s has a error\n" % (out_name)
		print "########################################################\n"
		
print "########################################################\n"
print "All files are done\n" 
print "########################################################\n\n"
exit(0)
