#!/bin/bash

for dia in 17 18; do

  for hora in 00 12; do

    echo "baixando dados de mistura do solo"
    wget -c https://ftp.cptec.inpe.br/pesquisa/bramsrd/BRAMS_5.4/data-brams/soil-moisture/2016/GPNR/GL_SM.GPNR.201612"${dia}""${hora}".vfm.gz

   done
done
exit	
