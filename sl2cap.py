#!/usr/bin/env python3
#
##########################################################
# L2CAP server
##########################################################
#
#
import sys, json, os
import bluetooth as bt
import datetime as dt

server_sock=bt.BluetoothSocket( bt.L2CAP )
port = 1101  # from 1 to 32767  odd-numbers, 
             # 1 to 1023 are reserved, not to use in custom app
             # for PSM reserved 1-4095, dunamic 4097-32765
             # default packet lenght:  672 B, max lenght: 6553 B
             # use set_l2cap_mtu() to adjust mtu
header_size = 60 
mtu = 672

def getheader(data):
    '''
    # "H:<20c>\nT:<10c>\nC:<10c>\nL:<4c>\n"
    # Host max 20chr
    # Time max 10chr
    # Commacd max 10char
    # Lenght max 4 char  (max 9999 char lenght)
    #    8+40+4+8 = 60 char
    #    all headers max = 60 char
    '''
    h={}
    for n in range(0,4):
        h[data[n].strip().split(":")[0]] = data[n].strip().split(":")[1]
    return h

end=False

server_sock.bind(("",port))
server_sock.listen(1)
print( "L2CAP server start at port {}".format(port) )
while not end:
    client_sock,address = server_sock.accept()
    print( "\nAccepted connection from {}".format(address) )
#    data = client_sock.recv(mtu).decode().strip()
#    print( "DATA:\n{}\n".format(data) )
    try:
        data=client_sock.recv(mtu).decode().strip()
        header = getheader( data.splitlines() )
    except:
        print( "Link header error, close connection." )
    else:
        timestamp=int(dt.datetime.now().timestamp())
        client_sock.send("OK {}".format(timestamp))
        print( "H:{}, T:{}, C:{}, L:{}".format( header["H"], header['T'], header['C'], header['L'] ) )
        try:
            data = client_sock.recv(int(header['L'])+1).decode()
        except:
            print( "Link data error, close connection." )    
        else:
            if len(data)==int(header['L']):
                client_sock.send("OK")
                print(data)
            else:
                client_sock.send("ER")
                print("Data lenght ERROR, header {} , receive {} B".format(header['L'], len(data)))
    finally:        
        client_sock.close()
#        end=True

server_sock.close()