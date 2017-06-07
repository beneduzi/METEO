import numpy as np
import netCDF4
import math
import sys
from math import pi
from numpy import cos, sin, arccos, power, sqrt, exp, arctan2, argmin, argmax, arctan

#already loaded nc4 file
def CFS_get(latCFS,lonCFS,lat0,lon0):
    latvals = latCFS[:] * rad_factor
    lonvals = lonCFS[:] * rad_factor
    lat0_rad = lat0 * rad_factor
    lon0_rad = lon0 * rad_factor
    delX = (latvals[:]-lat0_rad)**2
    delY = (lonvals[:]-lon0_rad)**2
    minindexX = delX.argmin()  # 1D index of minimum element
    minindexY = delY.argmin()
    return(minindexX, minindexY)
#receives path to nc4 file and lat lon
def CFS_grab(cfs_file,lat0,lon0):
    rad_factor =  pi/180.0
    CFSfile = netCDF4.Dataset(cfs_file, 'r')
    latCFS = CFSfile.variables['latitude']
    lonCFS = CFSfile.variables['longitude']		
    latvals = latCFS[:] * rad_factor
    lonvals = lonCFS[:] * rad_factor
    lat0_rad = lat0 * rad_factor
    lon0_rad = lon0 * rad_factor
    delX = (latvals[:]-lat0_rad)**2
    delY = (lonvals[:]-lon0_rad)**2
    minindexX = delX.argmin()  # 1D index of minimum element
    minindexY = delY.argmin()
    CFSfile.close()
    return(minindexX, minindexY)
