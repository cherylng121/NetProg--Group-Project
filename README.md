# SECR3253 - Network Programming Group Assignment
## Network Automation with Ansible, Docker & NETCONF

> **Course**: SECR3253 Network Programming  
> **Deadline**: 6 July 2026

---

## 📋 Project Overview

This project automates network device configuration and Linux system information collection using **Ansible**, **Docker**, and **NETCONF**.

---

## 👥 Group Members & Roles

| No. | Name | Student ID | Role |
|-----|------|-----------|------|
| 1 | CORNELIA LIM ZHI XUAN | A23CS5044 ||
| 2 | LEONARD LEE SUEN YU | A23CS0101 ||
| 3 | LIM EN DHONG | A23CS0239 ||
| 4 | NG JIN EN | A23CS0146 ||
| 5 | TAN LI JI | A23CS0185 ||

---

## Ansible Playbook

The Ansible playbook for this project is stored in the `ansible/` folder.

This playbook performs the required network automation tasks:

- Configure IP address on the router interface
- Configure local user account
- Configure MOTD banner message
- Configure interface description
- Configure default static route
- Retrieve device information

Files included:

| File | Purpose |
| --- | --- |
| `ansible/configure_device.yml` | Main Ansible playbook for device configuration and verification. |
| `ansible/inventory.ini` | Stores the Cisco IOS XE device connection details. |
| `ansible/ansible.cfg` | Stores Ansible default settings for the lab environment. |
| `ansible/README.md` | Documents the Ansible task, requirements, and run command. |

To run the Ansible playbook:

```bash
cd ansible
ansible-playbook configure_device.yml
```
