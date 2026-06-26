# Task 3 - Ansible Playbook

This folder contains the Ansible solution for the SECR3253 Network Programming group assignment.

The playbook configures a Cisco IOS XE device using Ansible.

## Files

| File | Purpose |
| --- | --- |
| `configure_device.yml` | Main Ansible playbook for device configuration and verification. |
| `inventory.ini` | Stores the Cisco IOS XE device connection details. |
| `ansible.cfg` | Sets the default inventory file and Ansible connection settings. |

## Configuration Tasks

The playbook performs the following tasks:

- Configure IP address on `GigabitEthernet2`
- Configure local user account
- Configure MOTD banner message
- Configure interface description
- Configure default static route
- Retrieve device information

## Requirements

Install Ansible and the required Cisco collections:

```bash
pip install ansible
ansible-galaxy collection install cisco.ios ansible.netcommon
