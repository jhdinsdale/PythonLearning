import time
import os, sys
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
localList = ["1", "2", "3", "4"]
remoteList = ["3", "4"]
snapPath = pool + "@" + snapPrefix
lastCommonSnap = snapPath + "lastCommonTime"
nextSnap = snapPath + cTime


# Zfs args
zListA = ["list", "-H", "-o name", "-t snapshot"]
zSendA = ["send", "-I", lastCommonSnap, nextSnap]
zRecvA = ["receive", "-Fnv", destination]
# Other args
sshArgs = [user, "@", host]
grepArgs = ['"', snapPrefix, '"', "| tail", " -n1"]


sshC = "ssh " + ''.join(sshArgs)
grepC = "grep " + ''.join(grepArgs)


# Define the required commands
def zfsCommand(args):
        toolPlusArgs = "zfs " + ' '.join(args)
        return toolPlusArgs
        # subprocess.call(toolArgs)

def chkLatestSnap(zLA,i):
    NowSnap = zfsCommand(zLA) + " | grep " + '"' + i + '"'
    if not NowSnap:
        NowSnap = zfsCommand(zLA) + " | grep " + '"' + i + '"' + " | tail -n1"
        return NowSnap
    else:
        print "got to here"
        return NowSnap

def chkRemoteSnap(sshC,zLA,grp):
    rSnap = sshC + " " + zfsCommand(zLA) + grp
    return rSnap


def syncSnap(zSA,zRA):
    return zfsCommand(zSA) + " | " + sshC + " " + zfsCommand(zRA)

def compareLists(a, b):
    for item in a:
        if item in b:
            print cTime
            print item
            print "checkLatestSnap: " + chkLatestSnap(zListA,nextSnap) + item
            print "checkRemoteSnap: " + chkRemoteSnap(sshC,zListA,"grp") + item
            print "syncSnap: " + syncSnap(zSendA,zRecvA) + item
            continue
        print "Item not in list 2: '%s'" %(item)

if __name__ == '__main__':
    compareLists(localList,remoteList)
