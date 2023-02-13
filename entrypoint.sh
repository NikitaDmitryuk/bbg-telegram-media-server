#!/bin/bash
set -xe
version=$(cat version)
revision=1
architecture=all
package_dir="bbg-telegram-media-server_${version}-${revision}_${architecture}"
src_dir=src

sudo apt-get update && sudo apt-get install -y debmake dh-python python3-all
python3 -m pip install --upgrade pip
pip3 install --upgrade --force-reinstall setuptools

export SETUPTOOLS_USE_DISTUTILS=stdlib
python3 setup.py sdist

mv dist/bbg_telegram_media_server-${version}.tar.gz bbg-telegram-media-server-${version}.tar.gz
tar -xzmf bbg-telegram-media-server-${version}.tar.gz
mv bbg_telegram_media_server-${version} bbg-telegram-media-server-${version}
cd bbg-telegram-media-server-${version}
debmake -b ":python3"
cd ..

mv bbg-telegram-media-server-${version} ${package_dir}
# mv ${package_dir}/debian ${package_dir}/DEBIAN
# rm -rf ${package_dir}/DEBIAN/patches
# rm -rf ${package_dir}/DEBIAN/source

mkdir -p ${package_dir}/etc
mkdir -p ${package_dir}/etc/systemd/system

cp ${src_dir}/.bbg-telegram-media-server-conf ${package_dir}/etc
cp ${src_dir}/bbg-telegram-media-server.service ${package_dir}/etc/systemd/system
cp version ${package_dir}

# rm ${package_dir}/debian/control
# touch ${package_dir}/debian/control
# cat > ${package_dir}/debian/control <<EOF
# Source: bbg-telegram-media-server
# Section: python
# Priority: optional
# Maintainer: Nikita Dmitryuk <dmitryuk.nikita@gmail.com>
# Build-Depends: debhelper-compat (= 12), dh-python, python3-all, python3-setuptools
# Standards-Version: 4.5.0
# Homepage: https://github.com/NikitaDmitryuk/bbg-telegram-media-server
# X-Python3-Version: >= 3.2
# Package: bbg-telegram-media-server
# Architecture: ${architecture}
# Depends: minidlna, python3-libtorrent
# Multi-Arch: foreign
# Description: Telegram media server for Beaglebone Green board
# Version: ${version}
# EOF

cd ${package_dir}
dpkg-source -y --commit
debuild
cd ..

# dpkg-deb --build --root-owner-group ${package_dir}
