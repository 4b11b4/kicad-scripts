#!/bin/bash

# This script is used when:
# Similar symbols in the schematic vary and prevent a successful export of the
# BoM. For example, two resistors: one is properly from the kicad-library, and
# the other is from the rescue library.
# Because the symbols differ, 1_click_BoM exports them as different parts.
#
# This script is essentially a find and replace (via sed) for those parts.
# You can supply a directory as a parameter when running the script, and then
# all schematic (.sch) files will be subject to the sed commands below.

if [ -z "$1" ]; then
  dir=${PWD##*/}
  printf "***\nNo parameter entered.\nUsing name of current directory.\n***\n"
else
  dir=$1
  printf "Using directory: $dir\n"
  printf "***\nAll .sch files in this directory will modify symbols below. View the script to see.\n***\n"
fi

select yn in "Y" "N"; do
    case $yn in
        Y ) break;;
        N ) exit;;
    esac
done

printf "Rescuing...\n"
printf "$1\n"

# Verify the strings used for "sed" before running.
find $dir -type f -name "*.sch" -print0
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/comp-rescue:C_Small-Device/Device:C_Small/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/comp-rescue:R_Small-Device/Device:R_Small/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/comp-rescue:4013-4xxx/4xxx:4014/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/Device:R_US/Device:R_Small/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/comp-rescue:D_Small_ALT-Device/Device:D_Small/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/comp-rescue:D_Small-Device/Device:D_Small/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/comp-rescue:Q_NMOS_GDS-Device/Device:Q_NMOS_GDS/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/first_blox-eagle-import:CPOL-USE2-5/Device:CP/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/first_blox-eagle-import:1N4148DO35-10/Device:D_Small/g'

#find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's///g'
