#!/usr/bin/env bash

version=0.1
revision=1
architecture=armhf

package_dir="bbg-telegram-media-server_${version}-${revision}_${architecture}"
build_dir="build-$version"
package_bin_dir=${package_dir}/usr/local/bin

mkdir -p $build_dir
cp -r ../application/* $build_dir

mkdir -p $package_bin_dir

pyinstaller $build_dir/bbg-telegram-media-server.py --paths src --onefile --clean --distpath $package_bin_dir --specpath $build_dir --workpath $build_dir

mkdir ${package_dir}/DEBIAN
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
