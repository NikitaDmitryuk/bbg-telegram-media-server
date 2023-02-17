#!/bin/bash
set -xe
version=$(cat version)
revision=1
architecture=all
package_dir="bbg-telegram-media-server_${version}-${revision}_${architecture}"
src_dir=src
sudo apt-get update && sudo apt-get install -y build-essential dh-python python3-pip python3-all python3-setuptools
mkdir  ${package_dir}/tmp/bbg-telegram-media-server -p
cp ${src_dir} ${package_dir}/tmp/bbg-telegram-media-server -rp
cp setup.py ${package_dir}/tmp/bbg-telegram-media-server
cp version ${package_dir}/tmp/bbg-telegram-media-server
mkdir -p ${package_dir}/DEBIAN
cat > ${package_dir}/DEBIAN/control <<EOF
Source: bbg-telegram-media-server
Section: python
Priority: optional
Maintainer: Nikita Dmitryuk <dmitryuk.nikita@gmail.com>
Build-Depends: debhelper-compat (= 12), dh-python, python3-all, python3-setuptools, python3-venv
Standards-Version: 4.5.0
Homepage: https://github.com/NikitaDmitryuk/bbg-telegram-media-server
X-Python3-Version: >= 3.2
Package: bbg-telegram-media-server
Architecture: ${architecture}
Depends: minidlna, python3-libtorrent, python3-pip, python3-all, python3-setuptools, python3-venv
Multi-Arch: foreign
Version: ${version}
Description: Telegram media server for Beaglebone Green board
EOF
mkdir -p ${package_dir}/etc/bbg-telegram-media-server
mkdir -p ${package_dir}/etc/systemd/system
cp ${src_dir}/bbg-telegram-media-server.conf ${package_dir}/etc/bbg-telegram-media-server
cp ${src_dir}/bbg-telegram-media-server.service ${package_dir}/etc/systemd/system
cat > ${package_dir}/DEBIAN/postinst <<EOF
#!/bin/bash
set -xe
cd /tmp/bbg-telegram-media-server
python3 -m venv bbg-telegram-media-server-env
source bbg-telegram-media-server-env/bin/activate
pip3 install --upgrade pip
pip3 install --upgrade --force-reinstall setuptools
export SETUPTOOLS_USE_DISTUTILS=stdlib
python3 setup.py install
deactivate
systemctl daemon-reload
systemctl enable --now bbg-telegram-media-server
systemctl enable --now minidlna
rm -rf /tmp/bbg-telegram-media-server
EOF
chmod +x ${package_dir}/DEBIAN/postinst
dpkg-deb --build ${package_dir}
