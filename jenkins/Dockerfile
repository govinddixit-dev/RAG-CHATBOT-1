# Use official Jenkins LTS image as base
FROM jenkins/jenkins:lts

# Switch to root to install additional packages
USER root

# Install Docker CLI (official Docker repo) + AWS CLI v2 in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        unzip \
        gnupg \
        python3 \
        python3-pip \
        python3-venv && \
    # ── Docker CLI ──────────────────────────────────────────────────
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | \
        gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
        https://download.docker.com/linux/debian bookworm stable" | \
        tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce-cli docker-compose-plugin && \
    # ── AWS CLI v2 ──────────────────────────────────────────────────
    curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip && \
    unzip -q awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws && \
    # ── Cleanup ─────────────────────────────────────────────────────
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to Jenkins user
USER jenkins

# Expose Jenkins web UI + agent port
EXPOSE 8080 50000

# Default command
CMD ["jenkins.sh"]
