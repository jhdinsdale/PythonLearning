import time
# import os, sys
import subprocess


# This declares the needed variables
# (this will in future be declared # inside an external .conf file)
pool = "tank/TeamShares"
host = "192.168.11.31"
user = "root"
destination = pool
snapPrefix = ".snapshot_hourly-"

# This sets the current time using epoch gmtime
cTime = "%s" % (time.strftime("%Y-%m-%d-%H", time.gmtime()))

# Variables
localList = ["2015-03-15-1517", "2015-03-15-1617", "2015-03-15-1717", "2015-03-15-1817"]
remoteList = ["2015-03-15-1717", "2015-03-15-1817"]
lastCommonSnap = pool + "lastCommonTime"
sshC = "ssh " + user + '@' + host

# Zfs args
zListA = ["list", "-H", "-o name", "-t snapshot"]
zSendA = ["send", "-I", lastCommonSnap, pool]
zRecvA = ["receive", "-Fnv", destination]

# Other args
grepArgs = ['"', snapPrefix, '"', " | tail", " -n1"]
grepC = "grep " + ''.join(grepArgs)


# Define the required commands
def zfsCommand(args):
        toolplusargs = "zfs " + ' '.join(args)
        return toolplusargs
        # subprocess.call(toolArgs)


def chkLatestSnap(zLA,pool,i):
    nwstsnap = zfsCommand(zLA) + " | grep " + '"' + pool + "@" + snapPrefix + i + '"'
    if not nwstsnap:
        nwstsnap = zfsCommand(zLA) + " | grep " + '"' + pool + "@" + snapPrefix + i + '"' + " | tail -n1"
        return nwstsnap
    else:
        print "got to here"
        return nwstsnap

def chkRemoteSnap(sshC,zLA,grp):
    rSnap = sshC + " " + zfsCommand(zLA) + " | " + grp
    return rSnap


def syncSnap(zSA,zRA):
    return zfsCommand(zSA) + " | " + sshC + " " + zfsCommand(zRA)

def compareLists(a, b):
    for item in a:
        if item in b:
            print cTime
            print item
            print "checkLatestSnap: " + chkLatestSnap(zListA, pool, item)
            print "checkRemoteSnap: " + chkRemoteSnap(sshC, zListA, grepC)
            print "syncSnap: " + syncSnap(zSendA, zRecvA) + item
            continue
        print "Item not in list 2: '%s'" % item

if __name__ == '__main__':
    compareLists(localList, remoteList)
