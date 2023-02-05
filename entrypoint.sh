#!/bin/bash

set -xe

version=0.1
revision=1
architecture=armhf

package_dir="bbg-telegram-media-server_${version}-${revision}_${architecture}"
build_dir="build-$version"
package_bin_dir=${package_dir}/usr/local/bin
package_conf_dir=${package_dir}/etc

sudo dpkg --add-architecture armhf
sudo apt-get update
sudo apt-get install -y python3-pip python3-libtorrent python3-venv python3-dev

mkdir -p $build_dir
cp -r application/. $build_dir


python3 -m venv bbg-telegram-media-server-env
source bbg-telegram-media-server-env/bin/activate
pip3 install python-telegram-bot cython

cd $build_dir
# make
cd ..

deactivate

mkdir -p ${package_conf_dir}
cp ${build_dir}/.bbg-telegram-media-server-conf ${package_conf_dir}
mkdir -p ${package_bin_dir}
cp ${build_dir}/bbg-telegram-media-server ${package_bin_dir}
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
