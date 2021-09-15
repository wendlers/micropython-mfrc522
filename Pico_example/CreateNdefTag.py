from mfrc522 import MFRC522
from RfidAccess import RfidAccess
import utime


    
              
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)
access = RfidAccess()

print("")
print("Please place card on reader")
print("")

def checksum(data):
    crc = 0xc7
    for byte in data:
        crc ^= byte
        for _ in range(8):
            msb = crc & 0x80
            crc = (crc << 1) & 0xff
            if msb:
                crc ^= 0x1d
    return crc


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
                defaultKey = [255,255,255,255,255,255]
                firstSectorKey = [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5]
                nextSectorKey = [0xD3, 0xF7, 0xD3, 0xF7, 0xD3, 0xF7]

                #set MAD sector
                # first fill block permission
                access.setTrailerAccess(keyA_Write=access.KEYB,access_Read=access.KEYAB,access_Write=access.KEYB,
                                        keyB_Read=access.NEVER,keyB_Write=access.KEYB)
                access.setBlockAccess(access.ALLBLOCK, access_Read=access.KEYAB, access_Write=access.KEYB,
                                      access_Inc=access.NEVER, access_Dec=access.NEVER)
                block3 = access.fillBlock3(keyA=firstSectorKey,keyB=defaultKey)
                #Write the sector access                
                if reader.writeSectorBlock(uid,0,3,block3,keyA=defaultKey) == reader.ERR:
                    print("Writing MAD sector failed!")
                else:
                    print(".",end="")
                    b1 = [0x14,0x01,0x03,0xE1,0x03,0xE1,0x03,0xE1,0x03,0xE1,0x03,0xE1,0x03,0xE1,0x03,0xE1]
                    b1[0] = checksum(b1[1:])  # I know this is already ok but just to demonstrate the CRC
                    reader.writeSectorBlock(uid,0,1,b1,keyB=defaultKey)
                    b2 = [0x03,0xE1,0x03,0xE1,0x03,0xE1,0x03,0xE1,0x03,0xE1,0x03,0xE1,0x03,0xE1,0x03,0xE1]
                    reader.writeSectorBlock(uid,0,2,b1,keyB=defaultKey)
                    #set permission for all other sectors
                    access.setTrailerAccess(keyA_Write=access.KEYB,access_Read=access.KEYAB,access_Write=access.KEYB,
                                            keyB_Read=access.NEVER,keyB_Write=access.KEYB)
                    access.setBlockAccess(access.ALLBLOCK, access_Read=access.KEYAB, access_Write=access.KEYAB,
                                          access_Inc=access.KEYAB, access_Dec=access.KEYAB)
                    block3 = access.fillBlock3(keyA=nextSectorKey,keyB=defaultKey)
                    #Write all next sectors access
                    for sector in range(1,16):
                        if  reader.writeSectorBlock(uid,sector,3,block3,keyA=defaultKey) == reader.ERR:
                            print("\nWriting to sector ",sector," Failed!")
                            break
                        else:
                            print(".",end="")
                    #force sector 1 to be 1 record empty
                    block= 16 *[0]
                    block[2]=0xfe
                    if reader.writeSectorBlock(uid,1,0,block,keyB=defaultKey) == reader.ERR:
                        print("Unable to set first NDEF record!")
                print("\nDone.")
                
                previousCard=uid
                break
        else:
            PreviousCard=[0]
        utime.sleep_ms(50)                

except KeyboardInterrupt:
    print("Bye")



