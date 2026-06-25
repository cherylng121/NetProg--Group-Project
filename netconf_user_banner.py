from ncclient import manager
from ncclient.operations import RPCError
import xmltodict
import json
import os

#Connection parameters
HOST = os.getenv("DEVICE_HOST", "192.168.56.101")
PORT = int(os.getenv("DEVICE_PORT", "830"))
USER = os.getenv("DEVICE_USER", "cisco")
PASS = os.getenv("DEVICE_PASS", "cisco")

def connect():
    """
    Establish a NETCONF connection to the Cisco IOS-XE device.
    The iosxe device parameter enables IOS-XE specific support in ncclient.
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

#Configure user account
def configure_user_account(
        m,
        username="netadmin",
        privilege=15,
        secret="SecurePass123!"):
    """
    Create a local user account with privilege level 15.
    Uses the Cisco-IOS-XE-native YANG model.
    """
    payload = f"""
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <username>
          <name>{username}</name>
          <privilege>{privilege}</privilege>
          <secret>
            <encryption>0</encryption>
            <secret>{secret}</secret>
          </secret>
        </username>
      </native>
    </config>"""
    m.edit_config(target="running", config=payload)
    print(f"[OK] User account '{username}' (privilege {privilege}) configured.")