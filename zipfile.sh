#!/bin/bash

rm GeneraUsuarios.zip

mkdir GeneraUsuarios

cp genera.py README.txt LICENSE config.ini GeneraUsuarios

zip -r GeneraUsuarios.zip GeneraUsuarios -x "*.git*" -x "*/.DS_Store" -x "__MACOSX/*"

rm -rf GeneraUsuarios

 