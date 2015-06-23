import time
import os
import subprocess

# Declare variables (this will be inside a .conf file)
pool = "tank/TeamShares"
destination = pool
host = "192.168.11.31"
user = "root"
snapPrefix = ".snapshot_hourly-"

# Declare variables for this file
currentTime = "%s" % (time.strftime("%Y-%m-%d-%H", time.gmtime()))
snapPath = pool + "@" + snapPrefix

lastCommonSnap = snapPath + "lastCommonTime"
nextSnap = snapPath + currentTime

# Zfs command args
zfsListArgs = ["list", "-H", "-o name", "-t snapshot"]
zfsSendArgs = ["send", "-i", lastCommonSnap, nextSnap]
zfsReceiveArgs = ["receive", "-nv", destination]

# Other command args
sshArgs = [user, "@", host]
grepArgs = ["grep", snapPrefix, "tail", "-n1"]


# Grep command
########### Do this bit next ##############


sshCommand = "ssh "+ ''.join(sshArgs)




# Define the required commands
def zfsCommand(args):
        toolArgs = "zfs " + ' '.join(args)
        return toolArgs
        # subprocess.call(toolArgs)

def latestSnap(zLA,i):
    return zfsCommand(zLA) + " | grep " + '"' + i + "17\" " + " | tail -n1"

def remoteSnap(zSA,zRA):
    return zfsCommand(zSA) + " | " + sshCommand + " " + zfsCommand(zRA)


# Example of run through
print currentTime
print "Executing latestSnap: " + latestSnap(zfsListArgs,nextSnap)
print "Executing remoteSnap: " + remoteSnap(zfsSendArgs,zfsReceiveArgs)



#print zfsCommand(zfsSendArgs) + " | " + sshCommand + " " + zfsCommand(zfsReceiveArgs)

