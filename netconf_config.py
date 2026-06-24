from ncclient import manager
from ncclient.operations import RPCError
import xmltodict
import json
import os

# Connection parameters
HOST = os.getenv("DEVICE_HOST", "192.168.56.101")
PORT = int(os.getenv("DEVICE_PORT", "830"))
USER = os.getenv("DEVICE_USER", "cisco")
PASS = os.getenv("DEVICE_PASS", "cisco")


def connect():
    """
    Establish a NETCONF session with the IOS-XE device using ncclient.
    Port 830 is the standard NETCONF-over-SSH port (RFC 6242).
    hostkey_verify=False is used in lab environments (not for production).
    """
    print(f"\n[NETCONF] Connecting to {HOST}:{PORT} as '{USER}' ...")
    conn = manager.connect(
        host=HOST,
        port=PORT,
        username=USER,
        password=PASS,
        hostkey_verify=False,
        device_params={"name": "iosxe"},
        timeout=30,
    )
    print("[NETCONF] Session established successfully.")
    return conn