#!/bin/bash
export NCARG_ROOT=/usr/local/ncl-6.3.0
export PATH=$PATH:$NCARG_ROOT/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/ncl_6.3.0/lib
export NETCDF=/usr/bin
export PATH=$PATH:/usr/local/bin
export PATH=$PATH:/usr/local/opengrads/Contents

model_name=CFS
DIR=/p1-zar/gustavo/tempook_proc/${model_name}
modelo=${model_name}D10001
hh=00
aa=`date +%Y`
mm=`date +%m`
dd=`date +%d`
aa4=`date +%Y`

for ens in `seq 1 4` ; do
	
	if test ! -s ${DIR}/${aa}${mm}${dd}${hh}/$ens; then
		echo "CRIANDO DIRETORIO  ${DIR}/${aa}${mm}${dd}${hh}"
		mkdir -p ${DIR}/${aa}${mm}${dd}${hh}/$ens
	
	else
		  echo "DIRETORIO ${DIR}/${aa}${mm}${dd}${hh}/$ens CRIADO"
	fi

	cd ${DIR}/${aa}${mm}${dd}${hh}/$ens
	cp /p1-zar/gustavo/tempook_proc/CFS/CFS.ctl . 
	for vez in `seq 40 120` ; do
		down(){
   
			horas=$(expr $vez \* 6)
			dataf=$(date -u +%Y%m%d%H -d "12am + $horas hours")
			caminho=ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs/cfs.${aa}${mm}${dd}/${hh}/6hrly_grib_0$ens
			arq=flxf${dataf}.0$ens.${aa}${mm}${dd}${hh}.grb2
			arq2=${dataf}.grb2

			if test ! -s ${DIR}/${aa}${mm}${dd}${hh}/$ens/${arq2} ; then
				/usr/bin/wget ${caminho}${i}/${arq}
				mv ${arq} ${arq2}	
			fi
			if test  -s ${DIR}/${aa}${mm}${dd}${hh}/$ens/${arq2} ; then
			  vartest=`echo $(ls -l ${DIR}/${aa}${mm}${dd}${hh}/$ens/${arq2} | awk '{ print $5 }')`
			  tamanho=`curl -sI ${caminho}/${arq} | grep Content- | cut -d " " -f2 |tr -d '\r\n'`
#			  tamanho=`echo $(curl -sI ${caminho}/${arq} | grep Content-Length | awk '{print $2}')`
			  if [ ${vartest} != $tamanho ]  ; then
				echo "arquivo existe mas eh pequeno"
				/usr/bin/wget ${caminho}/${arq}
				mv ${arq} ${arq2}
				vartest=$(ls -l ${DIR}/${aa}${mm}${dd}${hh}/$ens/${arq2} | awk '{ print $5 }')
				if [ ${vartest} != $tamanho ]  ; then
				       echo "tentei abaixar o arquivo pela 2 vez e continua pequeno"
				       echo "deu merda no download do arquivo ${arq}"  > ${DIR}/log_error1_simul.txt
     				fi
  			  fi
		  	   
			fi

			}
down
down
/opt/opengrads/gribmap -i  ${model_name}.ctl
/opt/opengrads/lats4d.sh -q -format netcdf -vars pressfc dswrfsfc pratesfc ugrd10m vgrd10m tmp2m spfh2m -i ${model_name}.ctl -o ../${modelo}${dataf}${ens}
	done


done

#for vez in `seq 40 160` ; do
#   horas=`expr $vez \* 6`
#   dataf=`date "+%Y%m%d%H" -d "+${horas}hour"`
#   arq2=${dataf}.grb2
#done

#/p1-zar/gustavo/tempook_proc/CFS/2016101000/g2ctl ${arq2} > ${model_name}.ctl
#sleep 1

#cd ${DIR}/${aa}${mm}${dd}${hh}/$ens

#      /usr/local/opengrads/Contents/lats4d.sh -q -format netcdf -lat -56 7 -lon 279 330 -vars pressfc dswrfsfc pratesfc ugrd10m vgrd10m tmp2m spfh2m  -i ${model_name}.ctl -o ${modelo}${dataf}
#      /usr/bin/g2ctl.pl ${arq2}  > ${model_name}.ctl
#      /usr/local/opengrads/Contents/gribmap -i  ${model_name}.ctl

#if test  -s ${DIR}/${aa}${mm}${dd}${hh}/${i}/${modelo}${dataf}.nc ; then
#   aaant=`date -d "-2day" "+%Y"`
#   mmant=`date -d "-2day" "+%m"`
#   ddant=`date -d "-2day" "+%d"`
#   rm -rf  ${DIR}/${aaant}${mmant}${ddant}${hh}/${i}

#sleep 1

#   cd ${DIR}/${aa}${mm}${dd}${hh}/${i}
#   files=`ls ${modelo}*`
#   sudo ncrcat -O ${files} ${modelo}${i}${aa}${mm}${dd}${hh}.nc
#   sudo rm -fv /var/www/html/processamento/${modelo}${i}${aaant}${mmant}${ddant}${hh}.nc
#   rm -fv ${files}
#fi



