ftpdownload
===========

Since Python's ftplib.FTP.retrBinary just doesn't cut it.
This module instead uses ftplib.FTP.transfercmd.
Written for Python 2.7.

Features:
- shows progress bar,
- during download sends commands to keep connection alive
- if disconnected, it reconnects and starts downloads from point of disconnect
