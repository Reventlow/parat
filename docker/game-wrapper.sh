#!/bin/bash
# Game wrapper for SSH sessions.
# Runs the game and ensures the session terminates on exit.
# No shell access is possible — ForceCommand enforces this script.

# Ensure sensible terminal defaults
export TERM="${TERM:-xterm-256color}"

# Trap all signals — clean exit on any interruption
trap 'exit 0' INT TERM HUP QUIT PIPE

# Run the game
cd /opt/parat
python3 parat.py 2>/dev/null

# Game exited — disconnect immediately
exit 0
