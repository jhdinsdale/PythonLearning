import time
import subprocess

# declare variables (this will be inside a .conf file)
pool = "tank/TeamShares"
destination = pool
host = "192.168.11.31"
user = "root"

lastCommonSnap = pool + "@" + "placeHolder01"
nextSnap = pool + "@" +"placeHolder02"
sshArgs = [user,"@",host]

zfsListArgs = ["list","-H","-o name","-t snapshot"]
zfsSendArgs = ["send","-i",lastCommonSnap,nextSnap]
zfsReceiveArgs = ["receive","-nv",destination]


print "Current Time: %s" % (time.strftime("%Y-%m-%d", time.gmtime()))
#print zfsListArgs
#print zfsSendArgs
#print zfsReceiveArgs

def zfsCommand(args):
        tool = "zfs "
        toolArgs = tool + ' '.join(args)
        print "Executing: " + toolArgs
                #print "Executing: " + tool + ' '.join(args)
        return toolArgs
        #subprocess.call(toolArgs)


#zfsCommand(zfsListArgs)
#zfsCommand(zfsSendArgs)
#zfsCommand(zfsReceiveArgs)
sshCommand = "ssh "+ ''.join(sshArgs)

print zfsCommand(zfsSendArgs) + " | " + sshCommand + " " + zfsCommand(zfsReceiveArgs)

