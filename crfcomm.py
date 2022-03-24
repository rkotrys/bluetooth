#/usr/bin/env python3
#
import sys, json, os
import bluetooth as bt
import datetime as dt
from pathlib import Path

port = 3
bdaddr=None
hostname=os.uname()[1]
db_name=Path('db.json')
if len(sys.argv)<2:
    print( "Usege:\n{} <BT_dev_name> <string_to_send>\n".format( __file__ ) )
    quit(0)
else:
    target_name=sys.argv[1]
if not db_name.is_file():
    with open( db_name,'w' ) as f:
        ts=int(dt.datetime.now().timestamp())
        json.dump( { 'ts': ts, 'n2a': {}, 'a2n': {} }, f, indent=4 )
        print( "DataBase file {} is created.\n".format(db_name ))
with open( db_name,'r' ) as f:
    db = json.load(f)
if target_name in db['n2a']:
    target_address = db['n2a'][target_name]
    print("Target name {} is found in data base with address {}\n".format(target_name,target_address))
else:
    print("Target name {} is not in data base, look up in  nearby activated\n".format(target_name) )
    nearby_devices = bt.discover_devices()
    for bd_addr in nearby_devices:
        if target_name == bt.lookup_name( bd_addr ):
            bdaddr = bd_addr
            print( "found target bluetooth device {} with address {}\n".format( target_name, bdaddr ) );
            db['n2a'][target_name]=bd_addr
            db['a2n'][bd_addr]=target_name
            with open( db_name,'w' ) as f:
                json.dump( db, f, indent=4 )
            break
    if bdaddr == None:
        print( "Could not find {} bluetooth device nearby\n".format(target_name) );
        quit()
    else:
        target_address = bdaddr
        print("{} have address: {}\n".format(target_name, bdaddr))

if len(sys.argv)<3:
    buf = "[{}] Hello there !!\nquit".format(hostname)
else:
    buf = "[{}] {}\nquit".format(hostname,sys.argv[2])

sock=bt.BluetoothSocket( bt.RFCOMM )
sock.connect((target_address, port))
print( "connect to dev: {}, bdaddr: {} port: {}\n".format(target_name, target_address, port) )
sock.send("host {}\nts {}\nlenght {}".format(hostname,db['ts'],len(buf)))
rep=sock.recv(10).decode().trim().split(" ")
if rep[0]=='OK':
    print("Connected at {}".format(rep[1]));
    timestamp=int(dt.datetime.now().timestamp())
    sock.send(buf)
else:
    print("Link error: {}".format(rep[1]))    
sock.close()
