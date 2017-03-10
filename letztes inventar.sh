cd $( dirname "$0" )
libreoffice ./buchhaltung/$(ls -1 ./buchhaltung | tail -n 1) &
