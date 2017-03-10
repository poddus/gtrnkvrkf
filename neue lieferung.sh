#! /bin/bash
## make folder with today's date with "Verkauf" subfolder, create Inventar.ods and open it for editing

cd $( dirname "$0" )
cp ./template.ods ./buchhaltung/$(date +%F).ods
libreoffice ./buchhaltung/$(date +%F).ods &
