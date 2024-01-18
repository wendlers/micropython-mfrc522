from mfrc522 import MFRC522
from RfidAccess import RfidAccess
import utime

    
              
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)
access = RfidAccess()

print("")
print("Please place card on reader")
print("")



PreviousCard = [0]

try:
    while True:

        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if uid == PreviousCard:
                continue

            if stat == reader.OK:
                print("Card detected {}  uid={}".format(hex(int.from_bytes(bytes(uid),"little",False)).upper(),reader.tohexstring(uid)))
                firstSectorKey = [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5]
                nextSectorKey = [0xD3, 0xF7, 0xD3, 0xF7, 0xD3, 0xF7]
                defaultKey = [255,255,255,255,255,255]

                # set default access
                access.decodeAccess(0xff,0x07,0x80)
                block3 = access.fillBlock3(keyA=defaultKey,keyB=defaultKey)
                print("Reset Mad Sector (first sector)")
                #reset first sector
                reader.writeSectorBlock(uid,0,3,block3,keyB=defaultKey)
                #erase block1 and 2
                datablock = 16 * [0]
                reader.writeSectorBlock(uid,0,1,datablock,keyB=defaultKey)
                reader.writeSectorBlock(uid,0,2,datablock,keyB=defaultKey)

                #reset all other sectors
                for s in range(1,16):
                    # permission to default
                    print("Reset sector ",s)
                    reader.writeSectorBlock(uid,s,3,block3,keyB=defaultKey)
                    for b in range(3):
                        # put all data to zero block 0,1 and 2
                        reader.writeSectorBlock(uid,s,b,datablock,keyB=defaultKey)
                # ok dump new data
                print("\n---- Dump card using defaultkeyB [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]\n")
                reader.MFRC522_DumpClassic1K(uid, Start=0, End=64, keyB=defaultKey)
                PreviousCard = uid
                break
            else:
                pass
                #print("Authentication error")
        else:
            PreviousCard=[0]
        utime.sleep_ms(50)                

except KeyboardInterrupt:
    print("Bye")

print("Card done!")


