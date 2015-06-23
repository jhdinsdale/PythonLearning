import time
import os
import subprocess

# Declare variables (this will be inside a .conf file)
pool = "tank/TeamShares"
destination = pool
host = "192.168.11.31"
user = "root"
sshArgs = [user, "@", host]
snapPrefix = ".snapshot_hourly"

# Declare variable for this file
lastCommonSnap = pool + "@" + snapPrefix + "pHolder01"
nextSnap = pool + "@" + snapPrefix + "pHolder02"

zfsListArgs = ["list", "-H", "-o name", "-t snapshot"]
zfsSendArgs = ["send", "-i", lastCommonSnap, nextSnap]
zfsReceiveArgs = ["receive", "-nv", destination]

# Test print of time for snapshot
print "Current Time: %s" % (time.strftime("%Y-%m-%d", time.gmtime()))

# Define the required commands
def zfsCommand(args):
        tool = "zfs "
        toolArgs = tool + ' '.join(args)
        print "Executing: " + toolArgs
        return toolArgs
        # subprocess.call(toolArgs)


sshCommand = "ssh "+ ''.join(sshArgs)

# Example of run through
print zfsCommand(zfsListArgs)

print zfsCommand(zfsSendArgs) + " | " + sshCommand + " " + zfsCommand(zfsReceiveArgs)

