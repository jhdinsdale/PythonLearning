import time
import os
import subprocess

# This declares the needed variables (this will in future be inside a .conf file)
pool = "tank/TeamShares"
host = "192.168.11.31"
user = "root"
destination = pool
snapPrefix = ".snapshot_hourly-"

# Current time
cTime = "%s" % (time.strftime("%Y-%m-%d-%H", time.gmtime()))

# Variables
localList = []
remoteList = []
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


sshCommand = "ssh " + ''.join(sshArgs)
grepCommand = "grep " + ''.join(grepArgs)



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
        print "went to here"
        return NowSnap

def chkRemoteSnap(sshC,zLA,grp):
    remoteSnap = sshC + " " + zfsCommand(zLA) + grp
    return remoteSnap


def syncSnap(zSA,zRA):
    return zfsCommand(zSA) + " | " + sshCommand + " " + zfsCommand(zRA)

def compareLists(a, b):
    for item in a:
        if item in b: continue
            print cTime
            print "checkLatestSnap: " + chkLatestSnap(zListA,nextSnap)
            print "checkRemoteSnap: " + chkRemoteSnap(sshCommand,zListA,"grp")
            print "syncSnap: " + syncSnap(zSendA,zRecvA)# Do sync here
        print "Item not in list 2: '%s'" %(item)

