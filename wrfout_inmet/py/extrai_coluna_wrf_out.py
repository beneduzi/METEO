#!/usr/bin/python
# coding: utf-8

import numpy as np
import netCDF4
import math
import sys
import time
import calendar
import datetime
import os
from math import pi
from numpy import cos, sin, arccos, power, sqrt, exp,arctan2

## Entrada
path_wrf = (sys.argv[1])
filename = (sys.argv[2])
lat1 = (sys.argv[3])
lon1 = (sys.argv[4])
#gep = (sys.argv[5])
pic1 = (sys.argv[6])
pic2 = (sys.argv[7])
date2 = (sys.argv[8])
date3 = (sys.argv[9])
bk = 0

date0 = datetime.datetime.strptime(date2, '%Y%m%d%H')
date1 = datetime.datetime.strptime(date3, '%Y%m%d%H')
lat0 = float(lat1)
lon0 = float(lon1)
#utc0 = float(utc1)
z=0
zz=0
def tunnel_fast(latvar,lonvar,lat0,lon0):
    rad_factor = pi/180.0 # radianos
    latvals = latvar[::] * rad_factor # latitude longitude ==> numpy arrays
    lonvals = lonvar[::] * rad_factor
    ny, nx, nz = latvals.shape
    lat0_rad = lat0 * rad_factor
    lon0_rad = lon0 * rad_factor
    clat, clon = cos(latvals),cos(lonvals)
    slat, slon = sin(latvals),sin(lonvals)
    delX = cos(lat0_rad) * cos(lon0_rad) - clat * clon
    delY = cos(lat0_rad) * sin(lon0_rad) - clat * slon
    delZ = sin(lat0_rad) - slat
    dist_sq = delX**2 + delY**2  + delZ**2
    minindex_1d = dist_sq.argmin()  # 1D index do elemento minimo
    iz_min,ix_min,iy_min = np.unravel_index( minindex_1d, latvals.shape)
    return iz_min,ix_min,iy_min

if (-28 <= lat0 <= -14) and (-54 <= lon0 <= -36):
	diferenca = date1 - date0
	d2 = date0 + datetime.timedelta(days = diferenca.days )
	##
	for i in range(0, diferenca.days):
		print "###"
		print i
		print "###"

		for j in range(0, 20):
			gep = i+1
			d1 = date0 + datetime.timedelta(days = i)
			data = d1.strftime('%Y%m%d%H')
			data2 = d1.strftime('%Y-%m-%d_')
			path = "%s/%s/%sgep%02d_%s00:00:00" % (path_wrf, data, filename, gep, data2)
			data_q = data
			while os.path.isfile(path) != True:
				i += 1
				d1 = date0 + datetime.timedelta(days = i)
				data = d1.strftime('%Y%m%d%H')
				if d1 > d2:
					bk = 1
					break
				data2 = d1.strftime('%Y-%m-%d_')
				path = "%s/%s/%sgep%02d_%s00:00:00" % (path_wrf, data, filename, gep, data2)
			if bk == 1:
				data_inexistente = "Data nao existe %s \n" % (data_q)
				f = open('out/data_inexistente.txt', 'a')
				f.write(data_inexistente)
				f.close()
#				exit()
#				print "Data nao existe %s \n" % (data_q)
				break
			ncfile = netCDF4.Dataset(path, 'r')

# variaveis do netcdf
			latvar = ncfile.variables['XLAT'] #latitude e longitude
			lonvar = ncfile.variables['XLONG']
			cu_chuva = ncfile.variables['RAINC']
			scu_chuva = ncfile.variables['RAINNC']
			time = ncfile.variables['Times']
			tempk = ncfile.variables['T2']
			press = ncfile.variables['PSFC']
			q2 = ncfile.variables['Q2']

#indices das coordenandas
			iz,ix,iy = tunnel_fast(latvar, lonvar, lat0, lon0)

			max_i	= len(time)
			chuva	= np.full((max_i, 20),-999.9)
			chuva_c	= np.full((max_i, 20),-999.9)
			chuva_nc= np.full((max_i, 20),-999.9)
			tempc	= np.full((max_i, 20),-999.9)
			pressao	= np.full((max_i, 20),-999.9)
			q_2	= np.full((max_i, 20),-999.9)
			umidade	= np.full((max_i, 20),-999.9)
			teste1	= np.full((max_i+1, 20),-999.9)
			teste2	= np.full((max_i+1, 20),-999.9)
			teste3	= np.full((max_i+1, 20),-999.9)
			teste4	= np.full((max_i+1, 20),-999.9)
			teste5	= np.full((max_i+1, 20),-999.9)
			teste6	= np.full((max_i+1, 20),-999.9)
			teste7	= np.full((max_i+1, 20),0)
			teste8	= np.full((max_i+1, 20),0)
			saida	= np.full((max_i+1, 20),-999.9)

			if max_i < 14:
				chu	= np.full((14 + 1, 20),-999.9)
				tma	= np.full((14 + 1, 20),-999.9)
				tmi	= np.full((14 + 1, 20),-999.9)
				uma	= np.full((14 + 1, 20),-999.9)
				umi	= np.full((14 + 1, 20),-999.9)
			else:
				chu	= np.full((max_i + 1, 20),-999.9)
				tma	= np.full((max_i + 1, 20),-999.9)
				tmi	= np.full((max_i + 1, 20),-999.9)
				uma	= np.full((max_i + 1, 20),-999.9)
				umi	= np.full((max_i + 1, 20),-999.9)

			##
			for i in range(0, max_i):
				if i == 0:
					chuva[i,j] = cu_chuva[i,ix,iy] + scu_chuva[i,ix,iy]
				else:
					chuva[i,j] = (cu_chuva[i,ix,iy] + scu_chuva[i,ix,iy]) - (cu_chuva[i-4,ix,iy] - scu_chuva[i-4,ix,iy])
				tempc[i,j] = tempk[i,ix,iy] - 273.15
				pressao[i,j] = press[i,ix,iz] / 100
				q_2[i,j] = q2[i,ix,iz]
				a5 = 17.2693882 * (tempc[i,j]) / (tempc[i,j] + (273.15 - 35.86))
				umidade[i,j] = 100 * (q_2[i,j] / ((379.90516 /(pressao[i,j]*100 )) * exp(a5)))
			ncfile.close()
			a=0
			b=4
			##
			##
			for i in range(0, max_i):
				teste8[1,j] += 100
				teste7[j,1] += 100
				if i > 14:
					break
				if a < max_i:
					chu[i,j] = chuva[a,j]
					um = np.argmin(umidade[a:b,j])
					umi[i,j] = umidade[um + a,j]
					UM = np.argmax(umidade[a:b,j])
					uma[i,j] = umidade[UM + a,j]
					tm = np.argmin(tempc[a:b,j])
					tmi[i,j] = tempc[tm + a,j]
					TM = np.argmax(tempc[a:b,j])
					tma[i,j] = tempc[TM + a,j]

					teste1[i,j] = tma[i,j]
					teste2[i,j] = tmi[i,j]
					teste3[i,j] = uma[i,j]
					teste4[i,j] = umi[i,j]
					teste5[i,j] = pressao[i,j]
					teste6[i,j] = chu[i,j]
#					teste7[i,j] = tempc[i,j]
#					teste8[i,j] = umidade[i,j]
				else:
					chu[i,j]  = -999.9
					umi[i,j]  = -999.9
					uma[i,j]  = -999.9
					tmi[i,j]  = -999.9
					tma[i,j]  = -999.9

					teste1[i,j] = -999.9
					teste2[i,j] = -999.9
					teste3[i,j] = -999.9
					teste4[i,j] = -999.9
					teste5[i,j] = -999.9
					teste6[i,j] = -999.9
#					teste7[i,j] = -999.9
#					teste8[i,j] += 100 


				a += 4
				b += 4
			##
#				print teste8[i,1]
#				print teste8[i,2]
#				print teste8[i,3]
#				print teste8[i,4]
#				print teste8[i,5]
#				print teste8[i,6]
#				print teste8[i,7]
#				print teste8[i,8]
#				print teste8[i,9]
#				print teste8[i,19]
#				print "################"

#############################################################################################################
		pasta_de_saida    = "/DATA/CROPNET/ENSEMBLE/WRFGEFS/" + data
		arquivo_de_saida1 = "/DATA/CROPNET/ENSEMBLE/WRFGEFS/" + data + "/teste_RAIN_" + pic1 + "_" + pic2 + "_" + data + ".asc"
		arquivo_de_saida2 = "/DATA/CROPNET/ENSEMBLE/WRFGEFS/" + data + "/teste_URMI_" + pic1 + "_" + pic2 + "_" + data + ".asc"
		arquivo_de_saida3 = "/DATA/CROPNET/ENSEMBLE/WRFGEFS/" + data + "/teste_URMA_" + pic1 + "_" + pic2 + "_" + data + ".asc"
		arquivo_de_saida4 = "/DATA/CROPNET/ENSEMBLE/WRFGEFS/" + data + "/teste_TMAX_" + pic1 + "_" + pic2 + "_" + data + ".asc"
		arquivo_de_saida5 = "/DATA/CROPNET/ENSEMBLE/WRFGEFS/" + data + "/teste_TMIN_" + pic1 + "_" + pic2 + "_" + data + ".asc"


		if os.path.isdir(pasta_de_saida) == True:
			np.savetxt(arquivo_de_saida1, chu[1:15], fmt='%4.2f')
			np.savetxt(arquivo_de_saida2, umi[1:15], fmt='%4.2f')
			np.savetxt(arquivo_de_saida3, uma[1:15], fmt='%4.2f')
			np.savetxt(arquivo_de_saida4, tma[1:15], fmt='%4.2f')
			np.savetxt(arquivo_de_saida5, tmi[1:15], fmt='%4.2f')
		else:
			os.makedirs("/DATA/CROPNET/ENSEMBLE/WRFGEFS/" + data)

			np.savetxt(arquivo_de_saida1, chu[1:15], fmt='%4.2f')
			np.savetxt(arquivo_de_saida2, umi[1:15], fmt='%4.2f')
			np.savetxt(arquivo_de_saida3, uma[1:15], fmt='%4.2f')
			np.savetxt(arquivo_de_saida4, tma[1:15], fmt='%4.2f')
			np.savetxt(arquivo_de_saida5, tmi[1:15], fmt='%4.2f')

#		z+=1
#		print "#########%.0f###########" % z


		np.savetxt('out/temp_max_wrf.txt', teste1[1:15], fmt='%4.2f')
		np.savetxt('out/temp_min_wrf.txt', teste2[1:15], fmt='%4.2f')
		np.savetxt('out/umidade_max_wrf.txt', teste3[1:15], fmt='%4.2f')
		np.savetxt('out/umidade_min_wrf.txt', teste4[1:15], fmt='%4.2f')
		np.savetxt('out/pressao_wrf.txt', teste5[1:15], fmt='%4.2f')
		np.savetxt('out/chuva_wrf.txt', teste6[1:15], fmt='%4.2f')
		np.savetxt('out/temperatura_wrf.txt', teste7[1:15], fmt='%4.2f')
	np.savetxt('out/umidade_wrf.txt', teste8[1:15,:] + teste7[1:15,:], fmt='%4.2f')
	print "####################FIM####################"
	##
else:
	out_of_range = '%s	lat:%f lon:%f Out of Range\n' % (pic1, lat0, lon0)
	f = open('out/out_of_range.txt', 'a')
	f.write(out_of_range)
	f.close()
	print "##Lat Lon erro##"
	exit()
