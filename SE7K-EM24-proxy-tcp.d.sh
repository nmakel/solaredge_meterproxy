#!/bin/bash
set +x
meinpfad=$(dirname $0)
file=/var/log/SE7K-EM24-proxy.log
logfile=$file
[ -e $file ] && [ $(stat --printf '%s' "$file") -gt 104857600 ] && rm "$file" 
file=/var/log/SE7K-EM24-proxy.err
errfile=$file
[ -e $file ] && [ $(stat --printf '%s' "$file") -gt 104857600 ] && rm "$file" 
nohup python3 $meinpfad/SE7K-EM24-proxy-tcp.py -c $meinpfad/SE-MTR-3Y-400V-A.conf 2>>$errfile >>$logfile &
