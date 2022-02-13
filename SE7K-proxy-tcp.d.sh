#!/bin/bash
set +x
meinpfad=$(dirname $0)
file=/var/log/modbus-proxy.log
[ -e $file ] && [ $(stat --printf '%s' "$file") -gt 104857600 ] && rm "$file" 
file=/var/log/modbus-proxy.err
[ -e $file ] && [ $(stat --printf '%s' "$file") -gt 104857600 ] && rm "$file" 
nohup python3 $meinpfad/SE7K-proxy-tcp.py -c $meinpfad/SE7K.conf 2>>/var/log/modbus-proxy.err >>/var/log/modbus-proxy.log &
