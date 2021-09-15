from mfrc522 import MFRC522

'''
BE AWARE that sectors(3,7,11,15,...,63) are access block.
if you want to change  (sector % 4) == 3 you should
know how keys and permission work!
'''



def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring

reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

print("")
print("Please place card on reader")
print("")

key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

try:
    while True:

        (stat, tag_type) = reader.request(reader.REQIDL)

        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                print(uid)
                print("Card detected %s" % uidToString(uid))
                reader.MFRC522_DumpClassic1K(uid,keyA=key)
                print("Test ! writing sector 2, block 0 (absolute block(8)")
                print("with [ 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 ]")
                absoluteBlock=8
                value=[]
                for i in range(16):
                    value.append(i)
                status = reader.auth(reader.AUTHENT1A, absoluteBlock, key, uid)
                if status == reader.OK:
                    status = reader.write(absoluteBlock,value)
                    if status == reader.OK:
                        reader.MFRC522_DumpClassic1K(uid,keyA=key)
                    else:
                        print("unable to write")
                else:
                    print("Authentication error for writing")
                break
except KeyboardInterrupt:
    print("Bye")


