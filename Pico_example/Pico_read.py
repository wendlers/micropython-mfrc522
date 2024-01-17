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
                
                if reader.IsNTAG():
                    print("Got NTAG{}".format(reader.NTAG))
                    reader.MFRC522_Dump_NTAG(Start=0,End=reader.NTAG_MaxPage)
                    #print("Write Page 5  to 0x1,0x2,0x3,0x4  in 2 second")
                    #utime.sleep(2)
                    #data = [1,2,3,4]
                    #reader.writeNTAGPage(5,data)
                    #reader.MFRC522_Dump_NTAG(uid,Start=5,End=6)
                else:
                    defaultKey = [255,255,255,255,255,255]
                    reader.MFRC522_DumpClassic1K(Start=0, End=64, keyA=defaultKey)
                PreviousCard = uid
            else:
                pass
        else:
            PreviousCard=[0]
        utime.sleep_ms(50)                

except KeyboardInterrupt:
    pass