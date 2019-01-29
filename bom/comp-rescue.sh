#!/bin/bash

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

printf "Rescuing...\n"
printf "$1\n"

find $dir -type f -name "*.sch" -print0
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/comp-rescue:C_Small-Device/Device:C_Small/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/comp-rescue:R_Small-Device/Device:R_Small/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/comp-rescue:4013-4xxx/4xxx:4014/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/Device:R_US/Device:R_Small/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/comp-rescue:D_Small_ALT-Device/Device:D_Small/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/comp-rescue:D_Small-Device/Device:D_Small/g'
find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's/comp-rescue:Q_NMOS_GDS-Device/Device:Q_NMOS_GDS/g'
#find $dir -type f -name "*.sch" -print0 | xargs -0 sed -i'' -e 's///g'
