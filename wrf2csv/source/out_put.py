#!/usr/bin/env python
#-*- coding:utf-8 -*-

import numpy as np
import sys
import os
import datetime

def _make_files(file_name, out_path, rain, temp_min, temp_max, date):

	out = []
	for i in range(0, len(date)):
		d2 = date[i].strftime('%d/%m/%Y')
		o1 = "%s; %s; %s; %s" % (d2, temp_max[i], temp_min[i], rain[i]) 
		out.append(o1)

	if os.path.isdir(out_path) == False:
		os.makedirs(out_path)
	file_name = "%s/%s.csv" % (out_path, file_name)
	file_ = open(file_name, 'a+')
	file_.write("\n".join(out))
	file_.close()
	eof = True
	
	return(eof)

def _get_name_date(path):
	try:
		file = path.split("/")[1]
	except:
		file = path.split("/")[0]
	file_name = file.split(".")[0]
	date = file_name.split("20101")[1]

	date0 = datetime.datetime.strptime(str(date), '%Y%m%d%H') 

	return(file_name, date0)
