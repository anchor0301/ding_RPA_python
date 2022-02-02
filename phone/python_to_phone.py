from ppadb.client import Client as AdbClient

from com.dtmilano.android.viewclient import ViewClient

client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
device = devices[0]
device.shell("am force-stop <package name>")

vc = ViewClient(*ViewClient.connectToDeviceOrExit())
vc.traverse()
