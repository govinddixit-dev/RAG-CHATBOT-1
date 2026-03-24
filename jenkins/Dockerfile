# Use official Jenkins LTS image as base
FROM jenkins/jenkins:lts

# Switch to root to install additional packages
USER root

# Install AWS CLI v2
RUN apt-get update && \
    apt-get install -y curl unzip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Docker CLI (for Docker-in-Docker if needed)
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to Jenkins user
USER jenkins

# Expose Jenkins port
EXPOSE 8080

# Default command
CMD ["jenkins.sh"]
