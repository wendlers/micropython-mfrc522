# micropython-mfrc522
(Micro)Python class to access the MFRC522 RFID reader

Basic class to access RFID readers of the type [MFRC522](http://www.nxp.com/documents/data_sheet/MFRC522.pdf). 
This is basically a re-write of [this](https://github.com/mxgxw/MFRC522-python) Python port for the MFRC522. I 
tried to strip things down and make them more "pythonic" so the result is small enough to run on 
[Micropython](https://github.com/micropython/micropython) boards. The only board I tried this so far is the 
[ESP8266](https://github.com/micropython/micropython/tree/master/esp8266). 

## Usage

Put the modules ``mfrc522.py``, ``examples/read.py``, ``examples/write.py`` to the root of the flash FS on your board. 
For the ESP8266 there are multiple solutions to do that. E.g. use the 
[WebREPL file transfer](https://github.com/micropython/webrepl), or [mpfshell](https://github.com/wendlers/mpfshell). 
 
The class expects the reader by default to be connected like this:

| Signal    | GPIO      | Note                                  |
| --------- | --------- | ------------------------------------- |
| sck       | GPIO0     |                                       |
| mosi      | GPIO2     |                                       |
| miso      | GPIO4     |                                       |
| rst       | GPIO5     |                                       |
| cs        | GPIO14    | Labeled SDA on most RFID-RC522 boards |
 
Now enter the REPL you could run one of the two exmaples: 

For detecting, authenticating and reading from a card:
 
    import read
    read.do_read()
    
This will wait for a MifareClasskic 1k card. As soon the card is detected, it is authenticated, and 
16 bytes are read from address 0x08.

For detecting, authenticating and writing to a card:

    import write
    write.do_write()

This will wait for a MifareClasskic 1k card. As soon the card is detected, it is authenticated, and 
16 bytes written to address 0x08.
