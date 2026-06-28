#!/bin/sh
set -e

echo "[entrypoint] Starting network automation container"

echo "[entrypoint] Running Ansible playbook (if present)"
if [ -f /workspace/ansible/configure_device.yml ]; then
  cd /workspace/ansible
  ansible-playbook configure_device.yml || echo "[entrypoint] Ansible playbook failed or returned non-zero exit"
  cd /workspace
else
  echo "[entrypoint] No Ansible playbook found in /workspace/ansible"
fi

echo "[entrypoint] Executing NETCONF Python scripts"
if [ -f /workspace/NetProg--Group-Project/netconf_user_banner.py ]; then
  python /workspace/NetProg--Group-Project/netconf_user_banner.py || echo "[entrypoint] netconf_user_banner failed"
fi

if [ -f /workspace/NetProg--Group-Project/netconf_config.py ]; then
  python /workspace/NetProg--Group-Project/netconf_config.py || echo "[entrypoint] netconf_config failed"
fi

echo "[entrypoint] Automation run complete. Keeping container open for debugging."
exec /bin/sh
