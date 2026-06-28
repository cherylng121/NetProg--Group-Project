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

## Dockerized Automation

Build the container (from project root):

```bash
docker build -t net-automator .
```

Run with Docker Compose (recommended):

```bash
DEVICE_HOST=192.168.56.101 DEVICE_USER=cisco DEVICE_PASS=cisco docker-compose up --build
```

Or run the container directly (host network used for simplicity):

```bash
docker run --rm -it \
	-e DEVICE_HOST=192.168.56.101 \
	-e DEVICE_PORT=830 \
	-e DEVICE_USER=cisco \
	-e DEVICE_PASS=cisco \
	--network host \
	-v "$PWD":/workspace \
	net-automator
```

The container will:

- Run the Ansible playbook at `ansible/configure_device.yml` against the device defined in `ansible/inventory.ini`.
- Execute the NETCONF Python scripts located in `NetProg--Group-Project/` to apply additional YANG-based changes and retrieve device information.

Environment variables `DEVICE_HOST`, `DEVICE_PORT`, `DEVICE_USER`, and `DEVICE_PASS` are used by the NETCONF scripts.

Quick Docker tips

- **Build** the image from the project root: `docker build -t net-automator .`.
- **Compose (recommended):** use `docker-compose up --build` to build and run; add `-d` to run detached.
- **Rebuild after changes:** `docker-compose build --no-cache` then `docker-compose up -d`.
- **View logs:** `docker-compose logs -f` or `docker logs -f net_automator`.
- **Stop and remove:** `docker-compose down`.

Notes

- Files in the repository are mounted into the container at `/workspace` so you can edit locally and re-run the container.
- If your environment uses strict networking, prefer running the container with access to the management network that reaches the device; the compose file uses host networking for convenience.
- To run only the NETCONF scripts directly (no Ansible):

```bash
python NetProg--Group-Project/netconf_user_banner.py
python NetProg--Group-Project/netconf_config.py
```


