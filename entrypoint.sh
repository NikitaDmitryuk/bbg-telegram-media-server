#!/bin/bash -e
set -euo pipefail

version=$(cat version)
revision=1
architecture=all
package_name="bbg-telegram-media-server"
base_dir="/opt/${package_name}"
package_dir="${package_name}_${version}-${revision}_${architecture}"
src_dir="src"
service_file="${src_dir}/bbg-telegram-media-server.service"
config_file="${src_dir}/bbg-telegram-media-server.conf"

# Установка необходимых зависимостей
sudo dpkg --add-architecture armhf
sudo apt-get update && sudo apt-get install -y patchelf ccache software-properties-common
sudo add-apt-repository 'deb [arch=armhf] http://ftp.debian.org/debian/ bullseye main contrib non-free'
sudo add-apt-repository 'deb [arch=armhf] http://security.debian.org/debian-security bullseye-security main contrib non-free'
sudo add-apt-repository 'deb [arch=armhf] http://ftp.debian.org/debian/ bullseye-updates main contrib non-free'
sudo apt-get update && sudo apt-get install -y libpython3.9-dev:armhf zlib1g-dev:armhf expat:armhf
sudo cp -r /usr/include/arm-linux-gnueabihf/ /usr/include/python3.9
sudo cp /usr/lib/python3.9/config-3.9-arm-linux-gnueabihf/libpython3.9-pic.a /usr/lib/python3.9/config-3.9-x86_64-linux-gnu/libpython3.9-pic.a
sudo ln -s /usr/lib/arm-linux-gnueabihf/libz.so /usr/lib/libz.so
sudo ln -s /usr/lib/arm-linux-gnueabihf/libexpat.so /usr/lib/libexpat.so
# find / -name libz.so || true
# exit 0
pip install poetry

python -m poetry config virtualenvs.create true
python -m poetry config virtualenvs.in-project true
python -m poetry install
python -m poetry run python -m nuitka --show-scons --standalone --onefile --follow-imports --output-filename=bbg-telegram-media-server bbg-telegram-media-server.py

exit 0

# Создание структуры каталогов для пакета
mkdir -p "${package_dir}/opt/${package_name}"
mkdir -p "${package_dir}/etc/${package_name}"
mkdir -p "${package_dir}/etc/systemd/system"
mkdir -p "${package_dir}/DEBIAN"

# Копирование исходного кода и ресурсов программы
cp -r "${src_dir}/bbg_telegram_media_server" "${package_dir}/opt/${package_name}"
cp setup.py "${package_dir}/opt/${package_name}"
cp version "${package_dir}/opt/${package_name}"
cp requirements.txt "${package_dir}/opt/${package_name}"
cp project.toml "${package_dir}/opt/${package_name}"
cp "${config_file}" "${package_dir}/etc/${package_name}"
cp "${service_file}" "${package_dir}/etc/systemd/system"

# Создание файла управления пакетом
cat > "${package_dir}/DEBIAN/control" <<EOF
Package: ${package_name}
Version: ${version}-${revision}
Section: python
Priority: optional
Architecture: ${architecture}
Maintainer: Nikita Dmitryuk <dmitryuk.nikita@gmail.com>
Depends: python3, python3-pip, python3-setuptools, python3-venv, minidlna, python3-libtorrent, libboost-tools-dev, libboost-python-dev
Description: Telegram media server for Beaglebone Green board
EOF

# Создание постинсталляционного скрипта
cat > "${package_dir}/DEBIAN/postinst" <<EOF
#!/bin/bash
set -e

# Создание и активация виртуального окружения Python
python3 -m venv "${base_dir}/venv"
source "${base_dir}/venv/bin/activate"

# Установка зависимостей Python
pip3 install --upgrade pip
pip3 install --upgrade --force-reinstall setuptools

# Установка python-libtorrent из исходников в виртуальное окружение
wget -qO- https://github.com/arvidn/libtorrent/releases/download/v2.0.8/libtorrent-rasterbar-2.0.8.tar.gz | tar xvz -C /tmp
cd /tmp/libtorrent-rasterbar-2.0.8
python3 -m pip install .
cd -
rm -rf /tmp/libtorrent-rasterbar-2.0.8

# Установка остальных зависимостей Python
pip3 install -r "${base_dir}/requirements.txt"

# Установка приложения с использованием pip
pip3 install "${base_dir}" --use-pep517

# Деактивация виртуального окружения Python
deactivate

# Настройка автозапуска сервиса
systemctl daemon-reload
systemctl enable --now bbg-telegram-media-server
systemctl enable --now minidlna

EOF



cat > "${package_dir}/DEBIAN/postrm" <<'EOF'
#!/bin/sh
# postrm script for bbg-telegram-media-server

set -e

case "$1" in
  remove|purge)
    # Удаляем каталог /opt/bbg-telegram-media-server при удалении или полном удалении пакета
    if [ -d /opt/bbg-telegram-media-server ]; then
      rm -rf /opt/bbg-telegram-media-server
    fi
    ;;
  *)
    echo "postrm called with unknown argument \`$1'" >&2
    exit 1
    ;;
esac

#DEBHELPER#

exit 0

EOF

chmod +x "${package_dir}/DEBIAN/postinst"
chmod +x "${package_dir}/DEBIAN/postrm"

# Создание Debian пакета
dpkg-deb --build "${package_dir}"
