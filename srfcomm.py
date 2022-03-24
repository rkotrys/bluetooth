#/usr/bin/env python3
#
import sys, json, os
import bluetooth as bt
import datetime as dt

server_sock=bt.BluetoothSocket( bt.RFCOMM )
port = 3

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
        data = client_sock.recv(255).decode().strip()
        print("DATA: ", data)
        d=data.splitlines()
        header={ d[0].strip().split(" ")[0]: d[0].strip().split(" ")[1], d[1].strip().split(" ")[0]: d[1].strip().split(" ")[1], d[2].strip().split(" ")[0]: d[2].strip().split(" ")[1]  }
    except:
        print( "Link header error, close connection." )
    else:
        timestamp=int(dt.datetime.now().timestamp())
        client_sock.send("OK {}".format(timestamp))
        print( "Sender: {}, ts: {}, lenght: {}".format( header["host"], header['ts'], header['lenght'] ) )
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
