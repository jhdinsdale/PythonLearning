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
lastCommonSnap = "pHolder01"
nextSnap = "pHolder02"

# Argument lists
# Zfs command
zfsListArgs = ["list", "-H", "-o name", "-t snapshot"]
zfsSendArgs = ["send", "-i", lastCommonSnap, nextSnap]
zfsReceiveArgs = ["receive", "-nv", destination]

# Ssh commands
sshArgs = [user, "@", host]
sshCommand = "ssh "+ ''.join(sshArgs)

# Grep command
########### Do this bit next ##############
grepArgs = ["grep", snapPrefix, "<TIME>", "tail", "-n1"]


# Test print of time for snapshot
print "Current Time: %s" % (time.strftime("%Y-%m-%d", time.gmtime()))

lastCommonSnap = pool + "@" + snapPrefix + "pHolder01"
nextSnap = pool + "@" + snapPrefix + "pHolder02"

# Define the required commands
def zfsCommand(args):
        tool = "zfs "
        toolArgs = tool + ' '.join(args)
        print "Executing: " + toolArgs
        return toolArgs
        # subprocess.call(toolArgs)



def latestSnap(zLA,i):
    return zfsCommand(zLA) + " | grep " + '"' + i + '" ' + "<TIME>" + " | tail -n1"

def remoteSnap(zSA,zRA):
    return zfsCommand(zSA) + " | " + sshCommand + " " + zfsCommand(zRA)

# Example of run through
print latestSnap(zfsListArgs,snapPrefix)
print remoteSnap(zfsSendArgs,zfsReceiveArgs)


#print zfsCommand(zfsSendArgs) + " | " + sshCommand + " " + zfsCommand(zfsReceiveArgs)

