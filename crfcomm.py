#/usr/bin/env python3
#
import sys, json, os
import bluetooth as bt
import datetime as dt
from pathlib import Path
import logging as log

log.basicConfig(level=log.DEBUG)

######################################
# service unic uuid (generated random)
service_name = "RFCOMM-rpi"
uuid = "104275c2-d062-4859-bf99-6cfd5f5ff199"
######################################

if len(sys.argv)<2:
    print( "Usege:\n{} <BT_dev_name> [string_to_send]\n".format( __file__ ) )
    quit(0)
else:
    target_name=sys.argv[1]

hostname=os.uname()[1]
log.debug("Search for BT service, uuid='{}'".format(uuid))
service_matches = bt.find_service( uuid = uuid )
if len(service_matches) == 0:
    log.info("Couldn't find the BT service, uuid='{}'".format(uuid))
    sys.exit(0)
else:    
    log.debug("Service uuid='{}' is found".format(uuid))
    
for first_match in service_matches:
    shostname = first_match["name"].split(' ')[1]
    if target_name==shostname or target_name=='eny':
        port = first_match["port"]
        service_name = first_match["name"]
        target_address = first_match["host"]
        log.debug("Service '{}' on host: {}, bdaddr: {} port: {} is found".format(target_name,service_name,target_address,port))
        break


sock=bt.BluetoothSocket( bt.RFCOMM )
sock.connect((target_address, port))
log.debug( "Connect to dev: {}, bdaddr: {} port: {}\n".format(target_name, target_address, port) )
if len(sys.argv)<3:
    buf = u"Hello there !!\n"
else:
    buf = u"{}".format(sys.argv[2])
timestamp=int(dt.datetime.now().timestamp())
sock.send("host:{}\nts:{}\ncmd:{}\nlenght:{}".format(hostname,timestamp,"DATA",len(buf)))
rep=sock.recv(64).decode().strip().split(" ")
if rep[0]=='OK':
    log.debug("Connected at {}\n".format(rep[1]));
    timestamp=int(dt.datetime.now().timestamp())
    
    sock.send(buf)
else:
    log.debug("Link error: {}".format(rep[2]))    
sock.close()
