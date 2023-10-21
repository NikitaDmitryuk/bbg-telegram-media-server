pkgbase=bbg-telegram-media-server
pkgname=('bbg-telegram-media-server')
pkgver=0.1
pkgrel=1
pkgdesc="Telegram bot for downloading torrent files"
arch=('armv7h')
url="https://github.com/NikitaDmitryuk/bbg-telegram-media-server"
license=('')
makedepends=('python' 'python-pip' 'nuitka')
depends=('minidlna')
options=(!strip)

prepare() {
  cd ..
  pip install python-telegram-bot libtorrent sqlite3
}

build() {
  cd ..
  python -m nuitka --standalone --onefile --follow-imports --noinclude-unittest-mode=allow --output-filename=bbg-telegram-media-server bbg-telegram-media-server.py
}

package() {
  cd ..
  mkdir -p ${pkgdir}/usr/bin
  mkdir -p ${pkgdir}/usr/lib/systemd/system
  mkdir -p ${pkgdir}/etc/bbg-telegram-media-server
  install bbg-telegram-media-server ${pkgdir}/usr/bin
  install -m644 bbg-telegram-media-server.service ${pkgdir}/usr/lib/systemd/system
  install -m644 bbg-telegram-media-server.conf ${pkgdir}/etc/bbg-telegram-media-server
}

pre_remove() {
	systemctl disable --now bbg-telegram-media-server
  systemctl disable --now minidlna
}

post_install() {
	systemctl enable --now bbg-telegram-media-server
  systemctl enable --now minidlna
}
