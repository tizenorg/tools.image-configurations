#!/bin/sh
#
#A simple script to batch generate all release-able images for MeeGo. 
#
#This script will check out all MeeGo Image Kickstart files and execute 
#image generation based on repository type selected for all release-able images. 
#
# Written for MeeGo by Chris Ferron <chris.e.ferron@linux.intel.com> based on an initial
# effort buy Anas Nashif.


ID=$1
REPOTYPE=$2
RELEASE=$3

# Preparation Section
#export http_proxy= http://XXX.XXX.XXX.XXX:XXXX/

rm -f *.log

if [ "$RELEASE" = "MeeGo1.1" ]; then
   git checkout -f MeeGo1.1 
elif [ "$RELEASE" = "Trunk" ]; then 
   git checkout -f master
else
   git checkout -f master
   echo "No release type given, default to Trunk. Current support is for Trunk and MeeGo1.1"
fi

git pull

if [ "$REPOTYPE" = "1" ]; then
  str="s/\@BUILD_ID\@/$ID/"
elif [ "$REPOTYPE" = "2" ]; then 
  str="s/\@BUILD_ID\@/preview/"
elif [ "$REPOTYPE" = "3" ]; then 
  str="s/\@BUILD_ID\@/daily/" 
else
 echo " Repository Type needs to be 1 for Weekly or 2 for Preview or 3 for Daily" 
 exit 1 
fi

find -name \*.ks -exec perl  -pi -e $str '{}' \;

# mk_image expects at minimal, one arg- the first arg must be the path to the ks file.
# all further args are passed through to 'mic create'
# finally, a --release argument is automatically prepended.
mk_image() {
   local ks="$1";
   shift
   local name="meego-$(basename "$ks")"
   name="${name%.ks}"
   local dirname="$(dirname "$ks")"
   rm -rf "${ID}/${dirname}/images/${name}"
   mic create -c "$ks" --release="${ID}" "$@" 2>&1 | tee "${name}-${ID}.log"
   if [ ! -d "${ID}/${dirname}/images/${name}" ]; then
      echo "error: no ${ID}/${dirname}/images/${name} directory created"
      return 1
   fi
   md5sum "${name}-${ID}.log" >> "${ID}/${dirname}/images/${name}/MANIFEST"
   cp "${name}-${ID}.log" "$ID/${dirname}/images/${name}/"
}


#Core Image Section
mk_image core/core-armv7l-n900.ks -f raw --save-kernel --arch armv7
mk_image core/core-armv7l-madde-sysroot.ks --format=fs --compress-disk-image=none --package=tar.bz2 --arch=armv7l --save-kernel
mk_image core/core-ia32-madde-sysroot.ks --format=fs --compress-disk-image=none --package=tar.bz2

#Netbook Image Section
mk_image netbook/netbook-ia32.ks -f livecd
mk_image netbook/netbook-ia32-qemu.ks --format=raw --compress-disk-image=none --package=tar.bz2

#IVI Image Section
mk_image ivi/ivi-ia32.ks -f livecd

#Handset Image Section
#mk_image handset/handset-ia32-aava-mtf.ks -f nand
mk_image handset/handset-ia32-mtf.ks -f nand
#mk_image handset/handset-ia32-aava-mtf-devel.ks -f nand
mk_image handset/handset-ia32-mtf-devel.ks -f nand
mk_image handset/handset-armv7l-n900.ks -f raw --save-kernel --arch=armv7l
mk_image handset/handset-armv7l-n900-devel.ks -f raw --save-kernel --arch=armv7l
mk_image handset/handset-armv7hl-n900.ks -f raw --save-kernel --arch=armv7hl
mk_image handset/handset-ia32-pinetrail-mtf.ks -f livecd
mk_image handset/handset-armv7l-qemu.ks --format=raw --compress-disk-image=none --package=tar.bz2 --arch=armv7l --save-kernel
mk_image handset/handset-ia32-qemu.ks --format=raw --compress-disk-image=none --package=tar.bz2
mk_image handset/handset-armv7l-madde-sysroot.ks --format=fs --compress-disk-image=none --package=tar.bz2 --arch=armv7l --save-kernel
mk_image handset/handset-ia32-madde-sysroot.ks --format=fs --compress-disk-image=none --package=tar.bz2

exit 0
