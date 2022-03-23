#/usr/bin/env python3
#
# L2CAP server

import bluetooth as bt

server_sock=bt.BluetoothSocket( bt.L2CAP )
port = 1101

end=False

server_sock.bind(("",port))
server_sock.listen(1)

while not end:
    client_sock,address = server_sock.accept()
    print( "Accepted connection from: {}\n".format(address) )

    data = client_sock.recv(1024).decode()
    print( "[{}] {}\n".format( address, data ) )
    client_sock.close()
    if data=='end':
        end=True

server_sock.close()
