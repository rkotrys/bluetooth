#/usr/bin/env python3
#
import sys
import bluetooth as bt

if len(sys.argv)<2:
    target_name = "RPI3A-05"
else:
    target_name=sys.argv[1]
target_address = None

nearby_devices = bt.discover_devices()

for bd_addr in nearby_devices:
    if target_name == bt.lookup_name( bd_addr ):
        bdaddr = bd_addr
        break

if bdaddr is not None:
    print( "found target bluetooth device with address {}\n".format( bdaddr ) );
else:
    print( "could not find target bluetooth device nearby\n" );

if len(sys.argv)<3:
    buf = "Hello there !!"
else:
    buf = sys.argv[2]

#bdaddr = "B8:27:EB:16:0D:4F"
port = 3

sock=bt.BluetoothSocket( bt.RFCOMM )

sock.connect((bdaddr, port))
print( "connect to dev: {}, bdaddr: {} port: {}\n".format(target_name, bdaddr, port) )
sock.send(buf)
sock.close()
