#!/bin/bash


N=$(cat /p1-zar/gustavo/Agrinet/ECMWF/INMET_ESTACOES.txt | wc -l)

cp /p1-zar/gustavo/Agrinet/ECMWF/INMET_ESTACOES.txt /home/gustavo/Downloads/ESTAC_INMET_

cat /home/gustavo/Downloads/ESTAC_INMET_ | tr -s ';' ' ' > /home/gustavo/Downloads/ESTAC_INMET__

for i in $(seq 1  $N);do
	 
	a=$(cat /home/gustavo/Downloads/ESTAC_INMET__ | awk '{print $1}'| head -1 | tr -d \")
	b=$(cat /home/gustavo/Downloads/ESTAC_INMET__ | awk '{print $4}'| head -1 | tr -d \")
	c=$(cat /home/gustavo/Downloads/ESTAC_INMET__ | awk '{print $5}'| head -1 | tr -d \")

	echo $a

	python /p1-zar/gustavo/Agrinet/ECMWF/py/ecmwf_csv.py /p1-zar/gustavo/ECWMF/NC/1979-2013.nc $b $c 0 19790101 > /p1-zar/gustavo/ECWMF/INMET/$a.txt
	sed -i 1d /home/gustavo/Downloads/ESTAC_INMET__
	done 

rm /home/gustavo/Downloads/ESTAC_INMET_* 

