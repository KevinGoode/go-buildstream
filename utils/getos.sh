#!/usr/bin/bash
# RUNME!!!
#This script gets a very small alpine OS. This cannot be used directly in buildstream since we need to remove dev dir.
#This script removes dev dir and retars image
#https://samthursfield.wordpress.com/2017/06/19/buildstream-and-host-tools/
#Simply run this script
rm *.tar.gz*
wget https://nl.alpinelinux.org/alpine/v3.6/releases/x86_64/alpine-minirootfs-3.6.1-x86_64.tar.gz

mkdir -p sysroot
tar -x -f alpine-minirootfs-3.6.1-x86_64.tar.gz -C sysroot --exclude=./dev
tar -z -c -f alpine-host-tools-3.6.1-x86_64.tar.gz -C sysroot .
rm alpine-minirootfs-3.6.1-x86_64.tar.gz
