#!/bin/bash
set -xe
version=$(cat version)
revision=1
architecture=any
package_dir="bbg-telegram-media-server_${version}-${revision}_${architecture}"
src_dir=src
package_bin_dir=${package_dir}/usr/local/bin
package_conf_dir=${package_dir}/etc

mkdir -p ${package_conf_dir}
cp ${src_dir}/.bbg-telegram-media-server-conf ${package_conf_dir}
mkdir -p ${package_dir}/DEBIAN
mkdir -p ${package_dir}/etc/systemd/system
cp ${src_dir}/bbg-telegram-media-server.service ${package_dir}/etc/systemd/system
touch ${package_dir}/DEBIAN/control

cat > ${package_dir}/DEBIAN/control <<EOF
Package: bbg-telegram-media-server
Version: ${version}
Architecture: ${architecture}
Depends: minidlna
Maintainer: Nikita Dmitryuk <dmitryuk.nikita@gmail.com>
Description: Telegram media server for Beaglebone Green board
EOF

dpkg-deb --build --root-owner-group ${package_dir}
