#!/bin/bash
# This script is to add some default text (i.e. "-") to fields which have
# been added to the Field Name Templates but are not actually written to
# the schematic.

# This was created because without these fields written to the .sch file, 
# KiField is unable to write values to these fields.

if [ -z "$1" ]; then
  dir=${PWD##*/}
  printf "***\nNo parameter entered.\nUsing name of current directory.\n***\n"
else
  dir=$1
  printf "Using directory: $dir\n"
fi

select yn in "Y" "N"; do
    case $yn in
        Y ) break;;
        N ) exit;;
    esac
done

printf "Adding fields...\n"
printf "$1\n"

find $dir -type f -name "*.sch" -print0
#find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's///g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/F\s3\s"~".*/F 3 "~" H 3000 2950 50  0001 C CNN\nF 4 "-" H 3000 2950 50  0001 C CNN "Power"\nF 5 "-" H 3000 2950 50  0001 C CNN "Description"\nF 6 "-" H 3000 2950 50  0001 C CNN "MFR"\nF 7 "-" H 3000 2950 50  0001 C CNN "MPN"\nF 8 "-" H 3000 2950 50  0001 C CNN "URL"\nF 9 "-" H 3000 2950 50  0001 C CNN "Sub"\nF 10 "-" H 3000 2950 50  0001 C CNN "Installed"\nF 11 "-" H 3000 2950 50  0001 C CNN "Note"\nF 12 "-" H 3000 2950 50  0001 C CNN "Composition"\nF 13 "-" H 3000 2950 50  0001 C CNN "Dielectric"\nF 14 "-" H 3000 2950 50  0001 C CNN "Tolerance"\nF 15 "-" H 3000 2950 50  0001 C CNN "Volt."/g'
