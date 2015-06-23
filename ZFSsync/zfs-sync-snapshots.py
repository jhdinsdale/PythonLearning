#!/bin/python

import time
import subprocess
# import os
# import sys

# This declares the required variables
# this will in future be declared inside an external .conf file
pool = "tank/TeamShares"
# the IPs of the master and slave zfs servers
master = "192.168.11.78"
slave = "192.168.11.31"
# the user with zfs permissions
user = "root"
# the prefix the snapshots will use
snapPrefix = ".snapshot_hourly-"

# The following variables are set internally and stay inline
# This sets the current time using epoch gmtime
cdate = "%s" % (time.strftime("%Y-%m-%d-%H", time.gmtime()))
ctime = "%s" % (time.strftime("%H:%M:%S", time.gmtime()))

# These are the two lists which will be populated and compared
# zfs list -H -o name -t snapshot > masterlist
masterlist = ['2015-03-15-2217', '2015-03-15-2317', '2015-03-16-0017', '2015-03-16-0117', '2015-03-16-0217']
# ssh user@slave zfs list -H -o name -t snapshot > slavelist
slavelist = ['2015-03-16-0017', '2015-03-16-0217']
# if in masterlist and in slavelist > cmbdlist
cmbdlist = []
# ZFS argument lists,
# list of ZFS List args
zla = ["list", "-H", "-o name", "-t snapshot"]
# list of ZFS Send args
zsa = ["send", "-I", 'firstmutualsnap', 'lastsnap_in_cmbdlist', pool]
# list of ZFS Receive args
zra = ["recv", "-Fnv", pool]


# Other declared variables and arguments
# ssh command to reach remote slave server from master server
sshslave = "ssh " + user + '@' + slave
# grep args
grepArgs = ['"', snapPrefix, '"', " | tail", " -n1"]
grepC = "grep " + ''.join(grepArgs)


# Here I define the required tools & commands
# This command joins the argument with the matching command
def zfsCommand(args):
    z = "zfs " + ' '.join(args)
    return z

# generating the two lists masterlist & slavelist
def zfsremote(sslave, args):
    zsl = sslave + ' ' + zfsCommand(args)
    return zsl

# This will perform a diff between the two lists masterlist & slavelist
# and add them to a new list
def diffLists():
    for item in masterlist:
        if item in slavelist:
            cmbdlist.append(item)
            continue
        # this will add to an error log with readable errors
        print item + ' not present in slavelist'
    return cmbdlist

if __name__ == '__main__':
    x = zfsCommand(zla)
    b = sshslave +  ' ' + zfsCommand(zla)
#    masterlist = subprocess.Popen(zfsCommand(zla), shell=True, stdout=subprocess.PIPE)
#    slavelist = subprocess.Popen(zfsremote(sshslave, zla), shell=True, stdout=subprocess.PIPE)
    print diffLists()
#    x = subprocess.Popen('ls -la /tmp', shell=True, stdout=subprocess.PIPE)
    print x
    print b


def find_remote_files(zla,sshsl):
    cmdline = sshsl + zla
    with open(os.devnull, "w") as devnull:
        proc = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=devnull)
        try:
            for entry in proc.stdout:
                items = entry.strip().split(None, 4)
                if not items[0].startswith("d"):
                    dt = datetime.strptime(" ".join(items[2:4]),
                                           "%Y/%m/%d %H:%M:%S")
                    yield (int(items[1]), dt, items[4])
            proc.wait()
        except:
            # On any exception, terminate process and re-raise exception.
            proc.terminate()
            proc.wait()
            raise