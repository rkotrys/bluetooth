#/usr/bin/env python3
#
import sys, json, os
import bluetooth as bt
import datetime as dt

server_sock=bt.BluetoothSocket( bt.RFCOMM )
port = 3

def getheader(data):
    h={}
    for n in range(0,4):
        h[data[n].strip().split(":")[0]] = data[n].strip().split(":")[1]
    return h

end=False

server_sock.bind(("",port))
server_sock.listen(1)
print( "RFCOMM server start at port {}".format(port) )
while not end:
    client_sock,address = server_sock.accept()
    print( "\nAccepted connection from {}".format(address) )
#    data = client_sock.recv(255).decode().strip()
#    print("DATA:\n", data)
    try:
        data=client_sock.recv(255).decode().strip()
        header = getheader( data.splitlines() )
        print( header )
    except:
        print( "Link header error, close connection." )
    else:
        timestamp=int(dt.datetime.now().timestamp())
        client_sock.send("OK {}".format(timestamp))
        print( "Sender: {}, ts: {}, cmd: {}, lenght: {}".format( header["host"], header['ts'], header['cmd'], header['lenght'] ) )
        try:
            data = client_sock.recv(int(header['lenght'])+2).decode()
        except:
            print( "Link data error, close connection." )    
        else:
            print(data)    
    finally:        
        client_sock.close()
#        end=True

server_sock.close()
