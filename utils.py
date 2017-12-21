import subprocess
import settings


def adb_connection_int(apps):
    '''
    Starts ADB server
    Connect to Device
    Kills All Apps
    '''
    adb = settings.ADB_BINARY
    dev_id = settings.DEVICE_ID
    subprocess.call([adb, "kill-server"])
    subprocess.call([adb, "start-server"])
    subprocess.call([adb, "-s", dev_id, "wait-for-device"])
    try:
        for app in apps:
            subprocess.call([adb, "shell", "am", "force-stop", app])
    except:
        pass


def adb_kill():
    """
    Kill ADB Server
    """
    adb = settings.ADB_BINARY
    subprocess.call([adb, "kill-server"])
