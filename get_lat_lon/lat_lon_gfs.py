import numpy as np
import netCDF4
import math
import sys
from math import pi
from numpy import cos, sin, arccos, power, sqrt, exp, arctan2, argmin, argmax, arctan

#already loaded nc4 file
def GFS_get(latGFS,lonGFS,lat0,lon0):
	latvals = latGFS[:] * rad_factor
	lonvals = lonGFS[:] * rad_factor
	lat0_rad = lat0 * rad_factor
	lon0_rad = lon0 * rad_factor
	delX = (latvals[:]-lat0_rad)**2
	delY = (lonvals[:]-lon0_rad)**2
	minindexX = delX.argmin()  # 1D index of minimum element
	minindexY = delY.argmin()
	return(minindexX, minindexY)

def GFS_grab(gfs_file,lat0,lon0):
	rad_factor =  pi/180.0
	GFSfile	= netCDF4.Dataset(gfs_file, 'r')
	latGFS	= GFSfile.variables['latitude']
	lonGFS	= GFSfile.variables['longitude']		
	latvals = latGFS[:] * rad_factor
	lonvals = lonGFS[:] * rad_factor
	lat0_rad = lat0 * rad_factor
	lon0_rad = lon0 * rad_factor
	delX	= (latvals[:]-lat0_rad)**2
	delY	= (lonvals[:]-lon0_rad)**2
	minindexX = delX.argmin()  # 1D index of minimum element
	minindexY = delY.argmin()
	GFSfile.close()
	return(minindexX, minindexY)

