from mfrc522 import MFRC522


def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring
    
              
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

print("")
print("Place card before reader to read from address 0x08")
print("")

try:
    while True:

        (stat, tag_type) = reader.request(reader.REQIDL)

        if stat == reader.OK:
    
            (stat, uid) = reader.SelectTagSN()
        
            if stat == reader.OK:
                print("Card detected %s" % uidToString(uid))
            else:
                print("Authentication error")

except KeyboardInterrupt:
    print("Bye")


