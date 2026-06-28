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

# Configure IP Address
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

# Configure Interface (no shutdown)
def configure_interface(m, interface="GigabitEthernet2"):
    """
    Enable an interface using Cisco IOS-XE native YANG.
    """
    iface_num = interface.replace("GigabitEthernet", "")
    payload = f"""
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>{iface_num}</name>
            <shutdown xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"
                      nc:operation="remove"/>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """

    m.edit_config(target="running", config=payload)
    print(f"[OK] Interface {interface} enabled (no shutdown).")

# Configure Static Route
def configure_static_route(m,
                            destination="0.0.0.0",
                            mask="0.0.0.0",
                            next_hop="10.10.10.254"):
    """
    Configure a static route using Cisco IOS-XE native YANG model.
    """
    payload = f"""
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
          <route>
            <ip-route-interface-forwarding-list>
              <prefix>{destination}</prefix>
              <mask>{mask}</mask>
              <fwd-list>
                <fwd>{next_hop}</fwd>
              </fwd-list>
            </ip-route-interface-forwarding-list>
          </route>
        </ip>
      </native>
    </config>
    """

    m.edit_config(target="running", config=payload)
    print(f"[OK] Static route {destination}/{mask} via {next_hop} configured.")

# ── Task 4: Retrieve Device Information ──────────────────────────────────────
def get_device_info(m):
    """
    Retrieve hostname and IOS version from the running configuration.
    """

    filter_xml = """
    <filter>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <version/>
        <hostname/>
      </native>
    </filter>
    """

    try:
        reply = m.get_config(
            source="running", 
            filter=("subtree", filter_xml)
            )
        
        data = xmltodict.parse(str(reply))

        native = (data.get("rpc-reply", {})
                      .get("data", {})
                      .get("native", {}))
        
        print("\n[Device Info]")
        print(f"  Hostname : {native.get('hostname', 'N/A')}")
        print(f"  Version  : {native.get('version', 'N/A')}")

    except RPCError as e:
        print(f"[WARN] Unable to retrieve filtered data: {e}")

# Main runner
def run():
    """Run all NETCONF_CONFIG tasks in sequence."""
    try:
        with connect() as m:
            configure_ip_address(m)
            configure_interface(m)
            configure_static_route(m)
            get_device_info(m)
    except Exception as e:
        print(f"[ERROR] NETCONF_CONFIG failed: {e}")
        raise

if __name__ == "__main__":
    run()