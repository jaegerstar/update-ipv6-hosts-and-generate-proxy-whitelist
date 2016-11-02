#!/usr/bin/env python
# coding =utf-8
# Anaconda3
 
import requests
import os
import time

path = 'c:\\Windows\\System32\\drivers\\etc\\'
file = 'hosts'

def getHosts(tryLimit=5):
    url = "https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts"
    chunk_size = 2048
    while tryLimit:
        r = requests.get(url)
        if r.status_code == 200:
            etag = r.headers['etag'].strip('"')
            with open(path+file, 'r') as f:
                local_etag = (f.readline().strip('#\n'))
            f.close
            if etag != local_etag:
                print 'There is a new hosts available, update it!'
                os.system('rename '+path+file+' '+'hosts.'+time.strftime("%Y-%m-%d.%H%M%S", time.localtime()))
                with open(path+file, 'wb') as fd:
                    fd.write('#'+etag+'\n')
                    for chunk in r.iter_content(chunk_size):
                        fd.write(chunk)
                fd.close
                os.system('ipconfig /flushdns')
                return 1
            else:
                print 'No newer hosts available, exit.'
                return 0
        else:
            tryLimit -= 1
 
 
def getDomain():
    if not getHosts():
        return "connection failed"
    print 'let\'s get domain'
    with open(path+file, 'r') as f:
        lines = f.readlines()
    with open('autoproxy-whitelist-for-byr.txt', 'wt') as f:
        f.write('[switchomega]\n')
        f.write('||bupt.edu.cn\n')
        f.write('||byr.cn\n')
        f.write('|http://10.\n')
        f.write('|https://10.\n')
        for line in lines:
            if line[0] == '#' or len(line) < 2:  # lazy
                continue
            line = line.split()
            if '.' in line[0]:
                continue
            f.write('||'+line[1].strip() + '\n')

if __name__ == '__main__':
    getDomain()
