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

#Configure MOTD banner
def configure_banner(
        m,
        message="Authorised access only. Disconnect immediately if not."):
    """
    Configure the Message of the Day (MOTD) banner.
    Uses the Cisco-IOS-XE-native YANG model.
    """
    payload = f"""
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <banner>
          <motd>
            <banner>{message}</banner>
          </motd>
        </banner>
      </native>
    </config>"""
    m.edit_config(target="running", config=payload)
    print("[OK] Banner MOTD configured.")

#Configure interface description
def configure_interface_description(
        m,
        interface="GigabitEthernet2",
        description="WAN Link - UTM SECR3253 Group Assignment"):
    """
    Configure the description for the selected interface.
    Uses the standard ietf-interfaces YANG model.
    """
    payload = f"""
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>{interface}</name>
          <description>{description}</description>
        </interface>
      </interfaces>
    </config>"""
    m.edit_config(target="running", config=payload)
    print(f"[OK] Interface {interface} description set.")

#Retrieve running configuration
def retrieve_running_config(m):
    """
    Retrieve and display selected information from the running configuration.
    Uses the NETCONF get-config operation with a subtree filter.
    """
    filter_xml = """
    <filter>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname/>
        <banner/>
        <username/>
        <interface/>
      </native>
    </filter>"""

    try:
        reply = m.get_config(source="running", filter=("subtree", filter_xml))
        data = xmltodict.parse(str(reply))
        native = (
            data.get("rpc-reply", {})
                .get("data", {})
                .get("native", {})
        )

        print("\n[Running Config - Key Sections]")

        for key in ["hostname", "banner", "username", "interface"]:
            if key in native:
                print(f"\n--- {key.upper()} ---")
                print(json.dumps(native[key], indent=4))

    except RPCError as e:
        print(f"[WARN] Filtered get-config failed: {e}")

        # Retrieve the full running configuration if the filter is not supported
        reply = m.get_config(source="running")

        print("[Running Config (first 800 characters)]")
        print(str(reply)[:800])

# Display NETCONF capabilities supported by the device
def show_capabilities(m):
    """
    Display the NETCONF capabilities advertised by the device.
    """
    caps = list(m.server_capabilities)

    print(f"\n[NETCONF Capabilities] ({len(caps)} total - showing first 10)")

    for cap in caps[:10]:
        print(f"  {cap}")

# Run all NETCONF tasks
def run():
    """
    Execute all NETCONF configuration tasks.
    """
    try:
        with connect() as m:
            show_capabilities(m)
            configure_user_account(m)
            configure_banner(m)
            configure_interface_description(m)
            retrieve_running_config(m)

    except Exception as e:
        print(f"[ERROR] NETCONF Task 2 failed: {e}")
        raise


if __name__ == "__main__":
    run()