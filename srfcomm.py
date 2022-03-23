#/usr/bin/env python3
#

import bluetooth as bt

server_sock=bt.BluetoothSocket( bt.RFCOMM )
port = 3

end=False

server_sock.bind(("",port))
server_sock.listen(1)

while not end:
    client_sock,address = server_sock.accept()
    print( "Accepted connection from ",address )

    data = client_sock.recv(1024).decode()
    print( "received {}".format( data ) )
    client_sock.close()
    if data=='end':
        end=True

server_sock.close()
