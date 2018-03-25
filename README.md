# micropython-mfrc522
(Micro)Python class to access the MFRC522 RFID reader

Basic class to access RFID readers of the type [MFRC522](http://www.nxp.com/documents/data_sheet/MFRC522.pdf). 
This is basically a re-write of [this](https://github.com/mxgxw/MFRC522-python) Python port for the MFRC522. I 
tried to strip things down and make them more "pythonic" so the result is small enough to run on 
[Micropython](https://github.com/micropython/micropython) boards. I tried the class so far on the 
[ESP8266](https://github.com/micropython/micropython/tree/master/esp8266) and 
the [WiPy](https://github.com/micropython/micropython/tree/master/cc3200). 

## Usage

Put the modules ``mfrc522.py``, ``examples/read.py``, ``examples/write.py`` to the root of the flash FS on your board. 
For the ESP8266 there are multiple solutions to do that. E.g. use the 
[WebREPL file transfer](https://github.com/micropython/webrepl), or [mpfshell](https://github.com/wendlers/mpfshell). 
 
I used the following pins for my setup:

| Signal    | GPIO ESP8266 | GPIO WiPy      | Note                                 |
| --------- | ------------ | -------------- | ------------------------------------ |
| sck       | 14           | "GP14"         |For hardware sck (esp)                |
| mosi      | 13           | "GP16"         |For hardware mosi (esp)               |
| miso      | 12           | "GP15"         |For hardware miso (esp)               |
| rst       | 2            | "GP22"         |                                      |
| cs        | 16           | "GP14"         |Labeled SDA on most RFID-RC522 boards |

Note for the hardware spi on the esp8266 the sck, mosi, and miso pins don't need to be specified for initalization,
only spiblk needs to be set to 1. In software mode they will need to be specified and spblk can be left unset.

Now enter the REPL you could run one of the two exmaples: 

For detecting, authenticating and reading from a card:
 
    import read
    read.do_read()  #for software
    read.do_read(1) #for esp hardware
    
This will wait for a MifareClassic 1k card. As soon the card is detected, it is authenticated, and 
16 bytes are read from address 0x08.

For detecting, authenticating and writing to a card:

    import write
    write.do_write()

This will wait for a MifareClassic 1k card. As soon the card is detected, it is authenticated, and 
16 bytes written to address 0x08.
