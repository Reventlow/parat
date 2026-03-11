#!/bin/bash
# Docker entrypoint: generate SSH host keys and start sshd.

# Generate host keys if not present (first run)
ssh-keygen -A 2>/dev/null

# Start SSH server in foreground
exec /usr/sbin/sshd -D -e
