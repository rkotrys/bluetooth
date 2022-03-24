#/usr/bin/env python3
#

import bluetooth as bt

server_sock=bt.BluetoothSocket( bt.RFCOMM )
port = 3

end=False

server_sock.bind(("",port))
server_sock.listen(1)
print( "RFCOMM server start at port {}".format(port) )
while not end:
    client_sock,address = server_sock.accept()
    print( "\nAccepted connection from {}".format(address) )
    data = client_sock.recv(255).decode()
    print("DATA: ", data)
#    try:
#        data = client_sock.recv(255).decode().trim()
#        print("DATA: ", data)
#        d=data.splitlines()
#        header={ d[0].trim().split(" ")[0]: d[0].trim().split(" ")[1], d[1].trim().split(" ")[0]: d[1].trim().split(" ")[1], d[2].trim().split(" ")[0]: d[2].trim().split(" ")[1]  }
#    except:
#        print( "Link header error, close connection." )
#    else:
#        print( "Sender: {}, ts: {}, lenght: {}".format( header["hostname"], header['ts'], header['lenght'] ) )
#        try:
#            data = client_sock.recv(header['lenght']+1).decode()
#        except:
#            print( "Link data error, close connection." )    
#        else:
#            print(data)    
#    finally:        
    client_sock.close()
    end=True

server_sock.close()
