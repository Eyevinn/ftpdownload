# coding=utf-8
__author__ = 'Fredrik Johansson'

import ftplib
import socket
import time
import datetime
import sys

def log(s):
    print '%s : %s'%(datetime.datetime.now(), s)
    sys.stdout.flush()
    sys.stderr.flush()

class client:
    def __init__(self, host, port, login, passwd):
        self.host = host
        self.port = port
        self.login = login
        self.passwd = passwd
        self.max_attempts = 5


    def downloadFile(self, filename, local_filename = None):
        if local_filename is None:
            local_filename = filename
        ftp = ftplib.FTP()
        ftp.set_debuglevel(0)
        ftp.set_pasv(True)

        def progressBar(bytes_for_a_dot, dot_bytes) :
            while dot_bytes > bytes_for_a_dot :
                sys.stdout.write('.')
                sys.stdout.flush()
                dot_bytes -= bytes_for_a_dot 
            return dot_bytes

        with open(local_filename, 'w+b') as f :
            while True :
                try :
                    ftp.connect(self.host, self.port)
                    ftp.login(self.login, self.passwd)
                    ftp.voidcmd('TYPE I')
                    filesize = ftp.size(filename)
                    sys.stdout.write('%sMB : '%(filesize / 1024 /1024))
                    bytes_for_a_dot = filesize / 80
                    dot_bytes = 0
                    if f.tell() :
                        sock = ftp.transfercmd('RETR ' + filename, f.tell()) 
                    else :
                        sock = ftp.transfercmd('RETR ' + filename)
                    while True :
                        blocksize = 1024*1024 #But it always takes 64KB?
                        block = sock.recv(blocksize)
                        if not block:
                            break
                        ftp.voidcmd('NOOP')
                        previous = f.tell()
                        f.write(block)
                        dot_bytes = progressBar(bytes_for_a_dot, dot_bytes + f.tell() - previous)
                    sock.close()
                    print
                    if filesize == f.tell() :
                        return 1
                    else :
                        log("Filesize %s not matching FTP filesize %s" %(f.tell(),filesize))
                        raise
                except :
                    self.max_attempts -= 1
                    if self.max_attempts == 0:
                        log("Giving up")
                        return 0
                    log('Waiting 10 seconds')
                    time.sleep(10)
                    log('Reconnecting')

            ftp.close()
            return 1

