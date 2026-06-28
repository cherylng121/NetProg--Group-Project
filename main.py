import sys
import os
import argparse

# Ensure scripts/ directory is on the path when run from project root
sys.path.insert(0, os.path.dirname(__file__))

from netconf_config      import run as run_netconf1
from netconf_user_banner import run as run_netconf2
from linux_info          import run as run_linux

BANNER ="""
╔═══════════════════════════════════════════════════════════╗
║  SECR3253 Network Programming — Group Assignment          ║
║  UTM 2025/2026-2                                          ║
║  Network Automation: NETCONF + Docker + Ansible + Linux   ║
╚═══════════════════════════════════════════════════════════╝
"""

def separator(title):
    print("\n" + "─" * 57)
    print(f"  {title}")
    print("─" * 57)

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="SECR3253 Group Assignment — Network Automation"
    )
    parser.add_argument(
        "--linux",
        action="store_true",
        help="Run Linux info collector only (no NETCONF device required)"
    )
    parser.add_argument(
        "--netconf",
        action="store_true",
        help="Run NETCONF configuration tasks only (requires CSR1000v)"
    )
    args = parser.parse_args()

    if args.linux:
        # Linux info only
        run_linux()

    elif args.netconf:
        # NETCONF tasks only
        separator("NETCONF_CONFIG — IP Address, Interface, Static Route")
        run_netconf1()
        separator("NETCONF_USER_BANNER — User, Banner, Description, Get-Config")
        run_netconf2()

    else:
        # Full run: NETCONF first, then Linux info
        separator("NETCONF_CONFIG — IP Address, Interface, Static Route")
        run_netconf1()
        separator("NETCONF_USER_BANNER — User, Banner, Description, Get-Config")
        run_netconf2()
        separator("Linux System Information")
        run_linux()

    print("\n[DONE] All tasks completed.\n")

if __name__ == "__main__":
    main()
