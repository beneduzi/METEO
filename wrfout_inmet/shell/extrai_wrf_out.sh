#!/bin/bash
# coding: utf-8

#N=$(cat /DATA/CROPNET/DADOS/estac/estac_estacoes | wc -l)
N=$(cat /DATA/CROPNET/DADOS/estac/INMET_ESTACOES.txt | wc -l)
N1=$(ls -1 /DATA/WRFOUT_ensembleGEFS/ | wc -l)
#data_star=$(ls -1 /DATA/WRFOUT_ensembleGEFS/|head -1| awk -F/ '{print $1}')
data_star=$(ls -1 /DATA/WRFOUT_ensembleGEFS/|head -77|tail -1| awk -F/ '{print $1}')
data_end=$(ls -1 /DATA/WRFOUT_ensembleGEFS/|head -n `expr $N1 - 1` | tail -1 | awk -F/ '{print $1}')

#echo $N
echo "Total de estaçoes: $N"
echo "Data inicial: $data_star final: $data_end"
echo "Iniciando"
tempo=$(echo "scale=1; ($N * 20 * 0.7) / 60" | bc -l)
echo "tempo estimado: $tempo min"

for j in $(seq 1  $N);do
	pic=$(cat /DATA/CROPNET/DADOS/estac/estac_estacoes | awk '{print $1}'|head -$j| tail -1  )
	pic_name=$(cat /DATA/CROPNET/DADOS/estac/estac_estacoes | awk '{print $3}'|head -$j| tail -1)
	lat=$(cat /DATA/CROPNET/DADOS/estac/estac_estacoes | awk '{print $4}'| head -$j| tail -1)
	lon=$(cat /DATA/CROPNET/DADOS/estac/estac_estacoes | awk '{print $5}'| head -$j| tail -1)
	model_path=/DATA/WRFOUT_ensembleGEFS
	model_name=wrfout_d01_


	for i in $(seq -f '%02g' 1 20);do
		gep=gep$i
		python py/extrai_wrf_out.py $model_path $model_name $lat $lon $gep $pic $pic_name $data_star $data_end &
		sleep 0.7
		done
	done
