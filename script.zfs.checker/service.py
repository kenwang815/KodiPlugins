import time
import xbmc
import sys
import subprocess
import xbmcaddon
__addon__ = xbmcaddon.Addon()

header = "ZFS Check"

timeout = int(__addon__.getSetting("zfs.timeout"))*1000
sleeptime = int(__addon__.getSetting("zfs.sleeptime"))


def run():
    cmd = "zpool status -x"
    process = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    out, err = process.communicate()
    errcode = process.returncode
    return str("%s%s Code(%s)"%(out, err, errcode)).replace('\n','')

if __name__ == '__main__':
    monitor = xbmc.Monitor()

    try:
        subprocess.call(['zpool'])
    except:
        xbmc.executebuiltin("Notification (%s ,%s, %d)"%(header,'Error: ZFS not installed!',timeout))
        sys.exit(0)

    info = run().replace('\\n','')
    xbmc.executebuiltin("Notification (%s ,%s, %d)"%(header,info,timeout))

    while True:
        timeout = int(__addon__.getSetting("zfs.timeout"))*1000
        sleeptime = int(__addon__.getSetting("zfs.sleeptime"))

        if monitor.waitForAbort(sleeptime):
            break

        while xbmc.Player().isPlaying():
            monitor.waitForAbort(1)


        info = run()
        xbmc.executebuiltin("Notification (%s ,%s, %d)"%(header,info,timeout))
