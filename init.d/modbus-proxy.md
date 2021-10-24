die modbus-proxy datei muss in /etc/init.d als ausführbare datei kopiert werden.

systemctl start modbus-proxy
systemctl enable modbus-proxy

martin@raspberrypi:~ $ ps -ef |grep python
root       436     1 11 01:35 ?        00:00:44 python3 /home/martin/gitHubClones/solaredge_meterproxy/SE7K-proxy-tcp.py -c /home/martin/gitHubClones/solaredge_meterproxy/SE7K.conf
