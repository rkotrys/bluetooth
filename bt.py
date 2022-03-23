import bluetooth, sys

port = 5

print("argv: {}".format(len(sys.argv)) )
print(sys.argv)

if len(sys.argv)==1:
    print(" Usage: python3 bt.py < s|c server_name >\n" );
    quit( 0 )
if (sys.argv[1]=='c') and ( len(sys.argv)<3):
    print("c Usage: python3 bt.py < s|c server_name >\n" );
    quit( 0 )
else:
    if (sys.argv[1]!='c') and (sys.argv[1]!='s'):
        print("s Usage: python3 bt.py < s|c server_name >\n" );
        quit( 0 )

if sys.argv[1]=='s':
    # server
    print( "Server start on port {}.".format(port) )
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    server_sock.bind(("",port))
    server_sock.listen(1)
    client_sock,address = server_sock.accept()
    print( "Accepted connection from {}".format(address) )
    data = 'start'
    try:
        while len(data)>0:
            data = client_sock.recv(1024)
            if data[0]=='.':
                break
            print( "received: {}".format(data) )
    except bluetooth.BluetoothError as e:
        print( e )

    #client_sock.close()
    #server_sock.close()
    quit( 0 )
else:
    # client
    target_name=sys.argv[2]
    target_address = None
    while target_address==None:
        print("Start scanning devices\n")
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        for bdaddr in nearby_devices:
            print( "dev: {}, address: {}\n".format(bdaddr[1],bdaddr[0]) )
            if target_name == bdaddr[1]:
               target_address = bdaddr[0]
               break

    print("Server {} is founf, address: {}\n".format(target_name,target_address) )
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    print( "Connect to: {} [{}]\n".format(target_name, target_address) )
    sock.connect((target_address, port))
    print( "Connected!\n" )
    sock.send("hello!!")
    sock.send(".")

    #sock.close()
    quit( 0 )
