#!/usr/bin/env python
#-*- coding:utf-8 -*-

import numpy as np
import netCDF4
import math
import sys
import datetime

from math import pi
from numpy import cos, sin, arccos, power, sqrt, exp, arctan2, argmin, argmax, arctan

##Chuva
def _get_rain(WRFfile, ixWRF, iyWRF,  date0, utc):
	rain_cu = WRFfile.variables['RAINC']
	rain_ncu = WRFfile.variables['RAINNC']
	time = WRFfile.variables['Times']  
	max_i = len(time)

	rain_hour = []
	for i in range(0, max_i):
		if i == 0:
			rain_hour.append(rain_cu[i, ixWRF, iyWRF] +  rain_ncu[i, ixWRF, iyWRF])
		else:
			rain_hour.append((rain_cu[i, ixWRF, iyWRF] +  rain_ncu[i, ixWRF, iyWRF]) - (rain_cu[i - 1, ixWRF, iyWRF] + rain_ncu[i - 1, ixWRF, iyWRF]))

	maxx = max_i // 24
	date = []
	rain_day = []
	b=0
	a=24
	for i in range(0, maxx):
		if a >= max_i:
			break
		d1 = date0 + datetime.timedelta(hours = 6) + datetime.timedelta(days = i) + datetime.timedelta(hours = utc)	
		rain_day.append(sum(rain_hour[b:a]))
		date.append(d1)
		b = a
		a += 24
	return(date, rain_day)
##Temperatura
def _get_temp(WRFfile, ixWRF, iyWRF,  date0, utc):
	temp_k = WRFfile.variables['T2']
	time = WRFfile.variables['Times']  
	max_i = len(time)

	temp_hour = []
	for i in range(0, max_i):
		temp_hour.append(temp_k[i, ixWRF, iyWRF] - 273.15)
	maxx = max_i // 24
	date = []
	temp_day = []
	temp_max = []
	temp_min = []
	b=0
	a=24
	for i in range(0, maxx):
		if a >= max_i:
			break
		d1 = date0 + datetime.timedelta(hours = 6) + datetime.timedelta(days = i) + datetime.timedelta(hours = utc)		
		temp_day.append(np.mean(temp_hour[b:a]))
		temp_min.append(min(temp_hour[b:a]))
		temp_max.append(max(temp_hour[b:a]))
		date.append(d1)

		b = a
		a += 24

	return(date, temp_max, temp_min)

