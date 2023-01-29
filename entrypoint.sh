#!/bin/bash

set -xe

version=0.1
revision=1
architecture=armhf

package_dir="bbg-telegram-media-server_${version}-${revision}_${architecture}"
build_dir="build-$version"
package_bin_dir=${package_dir}/usr/local/bin

sudo dpkg --add-architecture armhf
sudo apt-get update
sudo apt-get install -y gcc-arm-linux-gnueabihf python3-pip python3-libtorrent python3-venv python3-dev libpython3-dev:armhf

mkdir -p $build_dir
ls
cp -r application/* $build_dir

mkdir -p $package_bin_dir

python3 -m venv bbg-telegram-media-server-env
source bbg-telegram-media-server-env/bin/activate
pip3 install python-telegram-bot cython

cd $build_dir

python3 bbg-telegram-media-server-build.py build_ext --inplace

cd ..

mkdir -p ${package_dir}/DEBIAN
touch ${package_dir}/DEBIAN/control

cat > ${package_dir}/DEBIAN/control <<EOF
Package: bbg-telegram-media-server
Version: ${version}
Architecture: ${architecture}
Depends: minidlna
Maintainer: Nikita Dmitryuk <dmitryuk.nikita@gmail.com>
Description: Telegram media server for Beaglebone Green board
EOF

mkdir -p ${package_dir}/etc/systemd/system
cp ${build_dir}/bbg-telegram-media-server.service ${package_dir}/etc/systemd/system

dpkg-deb --build --root-owner-group ${package_dir}
