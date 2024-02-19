#!/bin/bash
set +x
meinpfad=$(dirname $0)
file=/var/log/modbus-proxy.log
logfile=$file
[ -e $file ] && [ $(stat --printf '%s' "$file") -gt 104857600 ] && rm "$file" 
file=/var/log/modbus-proxy.err
errfile=$file
[ -e $file ] && [ $(stat --printf '%s' "$file") -gt 104857600 ] && rm "$file" 
nohup python3 $meinpfad/SE7K-proxy-tcp.py -c $meinpfad/SE7K.conf 2>>$errfile >>$logfile &

