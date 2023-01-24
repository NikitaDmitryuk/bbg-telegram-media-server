# bbg-telegram-media-server

Telegram bot for downloading torrent files.

## Installation

Create a movie folder with the following files:
    1. token.txt - telegram token
    2. password.txt - your password to interact with the bot

Then enable the services by specifying the path to the folder with the files. Other downloaded files will be in the same folder.

```bash
sudo systemctl enable --now minidlna.service
sudo systemctl enable --now bbg-telegram-media-server@"/path/to/files".service
```
