# micropython-mfrc522
(Micro)Python class to access the MFRC522 RFID reader

D.Perron
Feb. 2021
Add Raspberry Pi Pico compatibility

D.Perron
Sept 20 2019
Modification  to be able to read 7 and 10 BYTES RFID
P.S. I didn't test the write mode.



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

| Signal | GPIO ESP8266 | GPIO ESP32 | GPIO WiPy | GPIO Pico | Note                          |
| ------ | ------------ | ---------- | --------- | --------- | ----------------------------- |
| sck    | 0            | 18         | "GP14"    | "GP2"     |                               |
| mosi   | 2            | 23         | "GP16"    | "GP3"     |                               |
| miso   | 4            | 19         | "GP15"    | "GP4"     |                               |
| rst    | 5            | 22         | "GP22"    | "GP0"     |                               |
| cs     | 14           | 21         | "GP14"    | "GP1"     | SDA on most RFID-RC522 boards |
 
Now enter the REPL you could run one of the two exmaples: 

The Pico_write example has been added but be aware of

- The software treated the memory has 64 sectors of 16 Bytes.
- In reality the mifare card is 16 sectors of 4 block which are 16 byte.
  The Block 0,1 and 2 are data block. The block 3 is the access  block
- BE AWARE if you write sector (3,7,11,15...,63) then you should know what you do


