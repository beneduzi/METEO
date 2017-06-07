#!/usr/bin/python
# coding: utf-8

import numpy as np
import netCDF4
import math
import sys
import time
import calendar
import datetime
from math import pi
from numpy import cos, sin, arccos, power, sqrt, exp,arctan2

## Entrada
filename = (sys.argv[1])
lat1 =  (sys.argv[2])
lon1 =  (sys.argv[3])
utc1 = (sys.argv[4])
date1 = (sys.argv[5])

lat0 = float(lat1)
lon0 = 360 + float(lon1)
utc0 = float(utc1)
date0 = datetime.datetime.strptime(date1, '%Y%m%d')

ncfile = netCDF4.Dataset(filename, 'r')

#########################################################################################
#def tunnel_fast(latvar,lonvar,lat0,lon0):						#
#											#
#    rad_factor = pi/180.0 # radianos							#
#											#
#    latvals = latvar[::] * rad_factor # latitude longitude ==> numpy arrays		#
#    lonvals = lonvar[::] * rad_factor							#
#    ny,nx,nz = latvals.shape								#
#    lat0_rad = lat0 * rad_factor							#
#    lon0_rad = lon0 * rad_factor							#
#    clat,clon = cos(latvals),cos(lonvals)						#
#    slat,slon = sin(latvals),sin(lonvals)						#	
#    delX = cos(lat0_rad)*cos(lon0_rad) - clat*clon					#
#    delY = cos(lat0_rad)*sin(lon0_rad) - clat*slon					#
#    delZ = sin(lat0_rad) - slat;							#
#    dist_sq = delX**2 + delY**2 + delZ**2						#	
#    minindex_1d = dist_sq.argmin()  # 1D index do elemento minimo			#
#    iz_min,ix_min,iy_min = np.unravel_index( minindex_1d, latvals.shape)		#
#    return iz_min,ix_min,iy_min							#
#########################################################################################

def tunnel_fast(latvar,lonvar,lat0,lon0):
    rad_factor = pi/180.0
    latvals = latvar[:] * rad_factor
    lonvals = lonvar[:] * rad_factor
    lat0_rad = lat0 * rad_factor
    lon0_rad = lon0 * rad_factor
    delX = (latvals[:]-lat0_rad)**2
    delY = (lonvals[:]-lon0_rad)**2
    minindexX = delX.argmin()  # 1D index of minimum element
    minindexY = delY.argmin()
    return minindexX, minindexY

#########################################################################################
#	variaveis do ecmwf
time = ncfile.variables['time']
latvar = ncfile.variables['latitude'] #latitude e longitude
lonvar = ncfile.variables['longitude']

tempk = ncfile.variables['t2m'] #temperatura em k
#tempk_min = ncfile.variables['mn2t']
#tempk_max = ncfile.variables['mx2t']

#chuva_c = ncfile.variables['cp']
chuva_t = ncfile.variables['tp']

##########################################################################################
#indices das coordenandas

#iz,ix,iy = tunnel_fast(latvar, lonvar, lat0, lon0)
ix,iy = tunnel_fast(latvar, lonvar, lat0, lon0)
max_i = len(time) 

##########################################################################################
# calcula os resultados das variaveis e imprimi a tabela
#print "data, temperatura, temp_max, temp_min, chuva_total, chuva_convec"
print "data, temperatura, chuva"
for i in range(0, max_i):

	d1 = date0 + datetime.timedelta(hours = i*12 + utc0)
	hora = d1.strftime('%Y%m%d %H:%M')
	tempc = tempk[i,ix,iy] - 273.15
#	tempc_min = tempk_min[i,ix,iy] - 273.15
#	tempc_max = tempk_max[i,ix,iy] - 273.15
#	chuva_co = chuva_c[i,ix,iy] * 1000
	chuva_to = chuva_t[i,ix,iy] * 1000
#	if chuva_co < 0:
#		chuva_co = 0
	if chuva_to < 0:  
                chuva_to = 0 

#	print ''' %s; %.1f; %.1f; %.1f; %.2f; %.2f ''' % (hora, tempc, tempc_max, tempc_max, chuva_to, chuva_co)
	print ''' %s; %.1f; %.2f ''' % (hora, tempc, chuva_to)
ncfile.close()
