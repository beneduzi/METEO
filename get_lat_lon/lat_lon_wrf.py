import numpy as np
import netCDF4
import math
import sys
from math import pi
from numpy import cos, sin, arccos, power, sqrt, exp, arctan2, argmin, argmax, arctan

#already loaded nc4 file
#uses tunnel method for locating closest lat lon tuple
def WRF_get(latWRF, lonWRF, lat0, lon0):
    rad_factor = pi/180.0
    latvals = latWRF[::] * rad_factor
    lonvals = lonWRF[::] * rad_factor
    ny ,nx, nz = latvals.shape
    lat0_rad = lat0 * rad_factor
    lon0_rad = lon0 * rad_factor
    clat, clon = cos(latvals), cos(lonvals)
    slat, slon = sin(latvals), sin(lonvals)
    delX = cos(lat0_rad) * cos(lon0_rad) - clat * clon
    delY = cos(lat0_rad) * sin(lon0_rad) - clat * slon
    delZ = sin(lat0_rad) - slat;
    dist_sq = delX**2 + delY**2 + delZ**2
    minindex_1d = dist_sq.argmin()
    iz_min, ix_min, iy_min = np.unravel_index( minindex_1d, latvals.shape)
    return(iz_min, ix_min, iy_min)

def WRF_grab(wrf_file, lat0, lon0):
    WRFfile = netCDF4.Dataset(wrf_file, 'r')
    latWRF = GFSfile.variables['XLAT']
    lonWRF = GFSfile.variables['XLON']	
    rad_factor = pi/180.0
    latvals = latWRF[::] * rad_factor
    lonvals = lonWRF[::] * rad_factor
    ny ,nx, nz = latvals.shape
    lat0_rad = lat0 * rad_factor
    lon0_rad = lon0 * rad_factor
    clat, clon = cos(latvals), cos(lonvals)
    slat, slon = sin(latvals), sin(lonvals)
    delX = cos(lat0_rad) * cos(lon0_rad) - clat * clon
    delY = cos(lat0_rad) * sin(lon0_rad) - clat * slon
    delZ = sin(lat0_rad) - slat;
    dist_sq = delX**2 + delY**2 + delZ**2
    minindex_1d = dist_sq.argmin()
    iz_min, ix_min, iy_min = np.unravel_index( minindex_1d, latvals.shape)
    return(ix_min, iy_min)

