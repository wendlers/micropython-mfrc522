class RfidAccess:
    NEVER = 0
    KEYA = 1
    KEYB = 2
    KEYAB = 3
    ALLBLOCK = -1

    def __init__(self):
        self.C1 = 0
        self.C2 = 0
        self.C3 = 8
        self.C1_Inv = 15
        self.C2_Inv = 15
        self.C3_Inv = 7
        self.Valid=False

    def findAccessIndex(self,table,mask,accessbits):
        for i in range(8):
            if table[i] == accessbits:
                if (i & 1) == 0 :
                    self.C2 = self.C2 & ~mask
                else:
                    self.C2 = self.C2 | mask

                if (i & 2) == 0 :
                    self.C1 = self.C1 & ~mask
                else:
                    self.C1 = self.C1 | mask

                if (i & 4) == 0:
                    self.C3 = self.C3 & ~mask
                else:
                    self.C3 = self.C3 | mask

                self.C1_Inv = self.C1 ^ 0xf
                self.C2_Inv = self.C2 ^ 0xf
                self.C3_Inv = self.C3 ^ 0xf
                return True
        return False
        




    def setTrailerAccess(self,keyA_Write=KEYA, access_Read=KEYA,access_Write=KEYA,keyB_Read=KEYA,keyB_Write=KEYA):
        #C1 weight 2 , C2 weight 1 , C3 weight 4

        #                  Key A Wr   Access R   Access W    KeyB R     KEYB W
        access_Index = ( (self.KEYA, self.KEYA, self.NEVER, self.KEYA,self.KEYA),
                         (self.NEVER,self.KEYA,self.NEVER,self.KEYA,self.NEVER),
                         (self.KEYB, self.KEYAB,self.NEVER,self.NEVER,self.NEVER),
                         (self.NEVER,self.KEYAB,self.NEVER,self.NEVER,self.NEVER),
                         (self.KEYA,self.KEYA,self.KEYA,self.KEYA,self.KEYA),
                         (self.KEYB,self.KEYAB,self.KEYB,self.NEVER,self.KEYB),
                         (self.NEVER,self.KEYAB,self.KEYB,self.NEVER,self.NEVER),
                         (self.NEVER,self.KEYAB,self.NEVER,self.NEVER,self.NEVER))
        if self.findAccessIndex(access_Index,8, (keyA_Write,access_Read,access_Write,keyB_Read,keyB_Write)):
            return True
        else:
            print("Access Trailer method not possible")
        return False
    

    def setBlockAccess(self, blockID, access_Read=KEYAB, access_Write=KEYAB, access_Inc=KEYAB, access_Dec=KEYAB):
       # C1 weight 2 , C2 weight 1 , C3 weight 4
       #                  Key Read  Key Write  INCREment   decrement/transfer/etc
       access_Blk_idx=((self.KEYAB, self.KEYAB, self.KEYAB, self.KEYAB,None),
                       (self.KEYAB, self.NEVER, self.NEVER, self.NEVER,None),
                       (self.KEYAB, self.KEYB, self.NEVER, self.NEVER,None),
                       (self.KEYAB, self.KEYB, self.KEYB, self.KEYAB,None),
                       (self.KEYAB, self.NEVER, self.NEVER, self.KEYAB,None),
                       (self.KEYB, self.KEYB, self.NEVER, self.NEVER,None),
                       (self.KEYB, self.NEVER, self.NEVER, self.NEVER,None),
                       (self.NEVER, self.NEVER, self.NEVER, self.NEVER,None))

       if(blockID == self.ALLBLOCK):
           Mask = 7
       elif (BlockID<0) or (blockID >3):
           return false
       else:
           Mask = 1 << blockID

       if self.findAccessIndex(access_Blk_idx,Mask,( access_Read, access_Write, access_Inc, access_Dec, None)):
           return True
       else:
           print("**** Error Access Block method not possible")
       return False


    def encodeAccess(self):
        self.C1 = self.C1 & 0xf
        self.C2 = self.C2 & 0xf
        self.C3 = self.C3 & 0xf
        self.C1_INV = self.C1 ^ 0xf
        self.C2_INV = self.C2 ^ 0xf
        self.C3_INV = self.C3 ^ 0xf
        byte6 = self.C2_INV << 4 | self.C1_INV
        byte7 = self.C1 << 4 | self.C3_INV
        byte8 = self.C3 << 4 | self.C2
        return (byte6, byte7, byte8)


    def decodeAccess(self, byte6,byte7,byte8):
        self.C1_Inv = byte6 & 0xf
        self.C2_Inv = (byte6 & 0xf0) >> 4
        self.C3_Inv = byte7 & 0xf
        self.C1 = (byte7 & 0xf0) >> 4
        self.C2 = byte8 & 0xf
        self.C3 = (byte8 & 0xf0) >>4
        return ((self.C1 ^ self.C1_Inv) & (self.C2 ^ self.C2_Inv) & (self.C3 ^ self.C3_Inv)) & 0xf == 0xf
    
    def decodeAccessFromBlock3(self, block3):
        if len(block3)!= 16:
            return False
        return self.decodeAccess(block3[6],block3[7],block3[8])


    def showTrailerAccess(self):
        KeyAWrite = ['key A', 'never', 'key B', 'never', 'key A', 'key B', 'never', 'never']
        AccessRead = ['key A', 'key A', 'key A|B', 'key A|B', 'key A','key A|B','key A|B','key A|B' ]
        AccessWrite = ['never', 'never', 'never', 'never', 'key A', 'key B', 'key B', 'never']
        KeyBRead  = ['key A  data R/W', 'key A data R', 'never', 'never', 'key A data R/W', 'never', 'never', 'never']
        KeyBWrite = ['key A  data R/W', 'never', 'key B', 'never', 'key A data R/W', 'key B', 'never', 'never']

        index = 0

        if  self.C2 & 0x8 > 0:
            index = 1
        if self.C1 & 0x8 > 0:
            index = index + 2
        if self.C3 & 0x8 > 0:
            index = index + 4


        #print("TrailerAccess idx=",index)
        print('Access key A read  => never')
        print('Access key A write =>', KeyAWrite[index])
        print('Access key B read  =>', KeyBRead[index])
        print('Access key B write =>', KeyBWrite[index])
        print('Access bits  read  =>', AccessRead[index])
        print('Access bits  write =>', AccessWrite[index])


    def showBlockAccess(self,blockID):
        BlockRead = ['key A|B','key A|B','key A|B','key A|B','key A|B','key B', 'key B', 'never' ]
        BlockWrite = ['key A|B', 'never', 'key B', 'key B', 'never', 'key B','never', 'never']
        BlockIncrement = ['key A|B', 'never', 'never', 'key B', 'never', 'never', 'never', 'never']
        BlockDecrement = ['key A|B', 'never', 'never', 'key A|B', 'key A|B', 'never', 'never', 'never']
        if blockID == 3:
            self.showTrailerAccess()
        else:
           mask = 1 << blockID
           index = 0
           if (self.C2 & mask) > 0:
               index =1
           if (self.C1 & mask) > 0:
               index = index + 2
           if (self.C3 & mask) > 0:
               index = index + 4

           print("Block ", blockID, " read  =>", BlockRead[index])
           print("Block ", blockID, " write =>", BlockWrite[index])
           print("Block ", blockID, " Increment =>", BlockIncrement[index])
           print("Block ", blockID, " Decrement+ =>", BlockDecrement[index])

    def showAccess(self):
        print("/---------  SHOW ACCESS  ---------\\")
        AccessB = self.encodeAccess()
        print('Access Bytes (6,7,8)= (',hex(AccessB[0]),', ',hex(AccessB[1]),', ',hex(AccessB[2]),')')
        print('(C1, C2, C3) = (',hex(self.C1),', ',hex(self.C2),', ',hex(self.C3),')')
        for i in range(4):
            self.showBlockAccess(i)
        print("\\---------------------------------/")
        
        
    def fillBlock3(self,keyA=None,keyB=None,block=None):
        if block is None:
           block = 16*[0xff]
        if len(block) != 16:
           block = 16*[0xff]

        if keyA is not None:
            if len(keyA) == 6 :
                block[0:6]=keyA
                
        if keyB is not None:
            if len(keyB) == 6 :
                block[10:16]=keyB
        b6, b7, b8 = self.encodeAccess()
        block[6]=b6
        block[7]=b7
        block[8]=b8
        return block
         


if __name__ == "__main__":
    rfid = RfidAccess()


    print("\nEx: Decode access_bits  for [0xff, 0x07, 0x80]")
    if rfid.decodeAccess(0xFF,0x07,0x80):
        rfid.showAccess()
    else:
        print('Invalid Access')

    print("\n\nSet block 0 to 3 to be read by KEYA but R/W with KEYB")
    rfid.setBlockAccess(rfid.ALLBLOCK, access_Read=rfid.KEYAB, access_Write=rfid.KEYB, access_Inc=rfid.NEVER, access_Dec=rfid.NEVER)
    print("Set sector trailer to be only set by Key B");
    rfid.setTrailerAccess(keyA_Write=rfid.KEYB,access_Read=rfid.KEYAB,access_Write=rfid.KEYB,keyB_Read=rfid.NEVER,keyB_Write=rfid.KEYB)
    rfid.showAccess()



