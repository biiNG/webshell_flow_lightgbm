#!/bin/bash
#pcap_path = $1
#joy_path = $2
files=$(ls $1)
echo $files

for file in $files
do
  name=$1'/../joy_json/'$file'.json'
  finger_name=$1'/../finger_json/'$file'-finger.json'
  FILE=$1$file
  touch $finger_name
  bash $2/bin/joy -x $2/install_joy/options.cfg $FILE | gunzip > $name
  $2/fingerprinting/fingerprinter.py $FILE > $finger_name
done
