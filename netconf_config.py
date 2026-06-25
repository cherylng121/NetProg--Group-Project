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
    """Create a NETCONF session with the IOS-XE device."""
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

# Task 1: Configure IP Address
def configure_ip_address(
    m,
    interface="GigabitEthernet2",
    ip="10.10.10.1",
    prefix=24
):
    """
    Configure an IPv4 address using IETF interface models.
    """

    payload = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>{interface}</name>
          <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
            ianaift:ethernetCsmacd
          </type>
          <enabled>true</enabled>
          <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
            <enabled>true</enabled>
            <address>
              <ip>{ip}</ip>
              <prefix-length>{prefix}</prefix-length>
            </address>
          </ipv4>
        </interface>
      </interfaces>
    </config>
    """

    m.edit_config(target="running", config=payload)
    print(f"[OK] Configured {ip}/{prefix} on {interface}")
