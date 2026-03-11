FROM python:3.12-slim

# Install SSH server, then clean up
RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/run/sshd

# Create restricted game user (no shell, no password)
RUN useradd -m -s /bin/bash parat \
    && passwd -d parat

# SSH config — locked down, ForceCommand only
COPY docker/sshd_config /etc/ssh/sshd_config

# Copy game source
COPY src/ /opt/parat/

# Copy wrapper and entrypoint
COPY docker/game-wrapper.sh /opt/parat/game-wrapper.sh
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /opt/parat/game-wrapper.sh /entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
