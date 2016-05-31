#!/usr/bin/env bash

mpfshell -c "open ttyUSB0; cd flash/lib; put mfrc522.py; lcd examples; put read.py; put write.py; ls" -n
