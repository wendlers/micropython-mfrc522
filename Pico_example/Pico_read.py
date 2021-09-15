from mfrc522 import MFRC522
import utime


def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring
    
              
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

print("")
print("Please place card on reader")
print("")



PreviousCard = [0]

try:
    while True:

        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        #print('request stat:',stat,' tag_type:',tag_type)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if uid == PreviousCard:
                continue
            if stat == reader.OK:
                print("Card detected {}  uid={}".format(hex(int.from_bytes(bytes(uid),"little",False)).upper(),reader.tohexstring(uid)))
                defaultKey = [255,255,255,255,255,255]
                reader.MFRC522_DumpClassic1K(uid, Start=0, End=64, keyA=defaultKey)
                print("Done")
                PreviousCard = uid
            else:
                pass
        else:
            PreviousCard=[0]
        utime.sleep_ms(50)                

except KeyboardInterrupt:
    pass