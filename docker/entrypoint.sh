#!/bin/bash
# Docker entrypoint: generate SSH host keys and start sshd.

KEY_DIR="/etc/ssh/host-keys"

# If persistent volume is mounted, use those keys
if [ -d "$KEY_DIR" ]; then
    # Generate keys into persistent dir if not present (first run)
    if [ -z "$(ls -A "$KEY_DIR"/ssh_host_* 2>/dev/null)" ]; then
        ssh-keygen -A 2>/dev/null
        mv /etc/ssh/ssh_host_* "$KEY_DIR/" 2>/dev/null
    fi
    # Symlink persistent keys into /etc/ssh
    for key in "$KEY_DIR"/ssh_host_*; do
        ln -sf "$key" /etc/ssh/
    done
else
    # No volume — generate ephemeral keys
    ssh-keygen -A 2>/dev/null
fi

# Start SSH server in foreground
exec /usr/sbin/sshd -D -e
