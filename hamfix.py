# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time

def runcmd(cmd):
    chunks = cmd.split(" ")
    print(cmd)
    res = subprocess.run(chunks, stdout=subprocess.PIPE)
    return res.stdout.decode("utf-8")

def basecall():
    return runcmd("sudo hamachi")

def is_daemon_running():
    return 'does not seem to be running' not in basecall()

def is_logged_in():
    return 'logged in' in basecall()

def start_daemon():
    runcmd("sudo /etc/init.d/logmein-hamachi start")

def restart_daemon():
    output = basecall()
    pidline = output.split('\n')[1]
    if 'pid' in pidline:
        pid = int(pidline.split(':')[1].strip())
        runcmd("sudo kill {}".format(str(pid)))
    start_daemon()

def fix_once():
    runcmd("sudo hamachi logout")
    time.sleep(15)
    output = runcmd("sudo hamachi login")
    if 'failed' in output:
        restart_daemon()
    time.sleep(15)

def fix_if_needed():
    if is_daemon_running():
        if not is_logged_in():
            fix_once()
    else:
        start_daemon()
        time.sleep(10)
        fix_if_needed()

def main():
    while True:
        fix_if_needed()
        time.sleep(60)

if __name__ == '__main__':
    main()
