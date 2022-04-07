#/usr/bin/env python3
#
import sys, json, os
import bluetooth as bt
import datetime as dt
import logging as log

log.basicConfig(level=log.DEBUG)

######################################
# service unic uuid (generated random)
hostname=os.uname()[1]
service_name = "RFCOMM-rpi {}".format(hostname)
uuid = "104275c2-d062-4859-bf99-6cfd5f5ff199"
######################################


def getheader(data):
    h={}
    for n in range(0,4):
        h[data[n].strip().split(":")[0]] = data[n].strip().split(":")[1]
    return h

def get_available_RF_port():
    sock=bt.BluetoothSocket( bt.RFCOMM )
    for port in range(2,60):
        try:
            sock.bind(("",port))
        except bt.BluetoothError:
            log.debug( "Porty {} is not avaiable".format(port) )
            continue
        else:
            log.debug("Port {} is bind to BTSocket".format(port))
            return sock
    log.error("All ports are busy - quit!")
    sock.close()
    quit(10)    
    

#server_sock=bt.BluetoothSocket( bt.RFCOMM )
server_sock=get_available_RF_port()
server_sock.listen(1)

bt.advertise_service( server_sock, service_name,  service_id=uuid, service_classes=[bt.SERIAL_PORT_CLASS], profiles=[bt.SERIAL_PORT_PROFILE],provider=hostname,description='RPI-serial' )
log.debug( "RFCOMM server start at port {}".format(port) )
log.debug("Service Discovery Protocol advertise service as: ".format(service_name))
end=False
while not end:
    client_sock,address = server_sock.accept()
    log.debug( "\nAccepted connection from {}".format(address) )
#    data = client_sock.recv(255).decode().strip()
#    print("DATA:\n", data)
    try:
        data=client_sock.recv(255).decode().strip()
        header = getheader( data.splitlines() )
    except:
        log.debug( "Link header error, close connection." )
    else:
        timestamp=int(dt.datetime.now().timestamp())
        client_sock.send("OK {}".format(timestamp))
        log.debug( "Sender: {}, ts: {}, cmd: {}, lenght: {}".format( header["host"], header['ts'], header['cmd'], header['lenght'] ) )
        try:
            data = client_sock.recv(int(header['lenght'])+10).decode()
        except:
            log.error( "Link data error, close connection." )    
        else:
            print(data)    
    finally:        
        client_sock.close()
#        end=True

server_sock.close()
