#!/usr/bin/bash
#This alpine is small and apart from libpthread and libc it is capable of building go projects
#One strategy could be to download this, and then manually copy over  libpthread and libc
#then re-tar. See ref:
#https://samthursfield.wordpress.com/2017/06/19/buildstream-and-host-tools/
wget https://nl.alpinelinux.org/alpine/v3.6/releases/x86_64/alpine-minirootfs-3.6.1-x86_64.tar.gz

mkdir -p sysroot
tar -x -f alpine-minirootfs-3.6.1-x86_64.tar.gz -C sysroot --exclude=./dev
tar -z -c -f alpine-host-tools-3.6.1-x86_64.tar.gz -C sysroot .

