import requests, random, smtplib, telnetlib, sys, os, hashlib, base64, subprocess, time, xtelnet, os, threading  # ,requests_ntlm
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from ftplib import FTP
from ..common.payloads import *

if os.path.isdir("/data/data") == True:
    adr = True
if os.path.isdir("/data/data/com.termux/") == True:
    termux = True
import mysqlcp
from ..utils.pager import *
from ..scanners.cms.wp import wpadmin
from ..cryptographers.hasher import *
from ..utils.pager import *



def process_threaded(a, check_interval=0.1):
    while True:
        try:
            if a.done() == True:
                try:
                    return a.result
                except:
                    pass
                try:
                    return a.counter
                except:
                    return
            time.sleep(check_interval)
        except KeyboardInterrupt:
            a.stop = True
            try:
                return a.result
            except:
                pass
            try:
                return a.counter
            except:
                pass
