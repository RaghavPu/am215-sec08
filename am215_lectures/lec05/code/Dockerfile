# Use a standard Debian-based Python image for a comfortable dev environment
FROM python:3.11-slim

# Install system dependencies: git, compilers, docker-out-of-docker, and nice shell tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    neovim \
    bat \
    wget \
    unzip \
    file \
    less \
    curl \
    sxiv \
    gpg \
    ca-certificates \
    && \
    # Install eza from its official repo
    mkdir -p /etc/apt/keyrings && \
    wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc | gpg --dearmor -o /etc/apt/keyrings/gierens.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" > /etc/apt/sources.list.d/gierens.list && \
    apt-get update && apt-get install -y eza && \
    # Install yazi from pre-compiled binary
    YAZI_VERSION=0.2.4 && \
    wget https://github.com/sxyazi/yazi/releases/download/v${YAZI_VERSION}/yazi-x86_64-unknown-linux-gnu.zip -O /tmp/yazi.zip && \
    unzip /tmp/yazi.zip -d /tmp && \
    mv /tmp/yazi-x86_64-unknown-linux-gnu/yazi /usr/local/bin/yazi && \
    rm -rf /tmp/yazi.zip /tmp/yazi-x86_64-unknown-linux-gnu && \
    # Clean up apt cache
    rm -rf /var/lib/apt/lists/*

# Install Docker CLI (for Docker-out-of-Docker)
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN chmod a+r /etc/apt/keyrings/docker.gpg
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update && apt-get install -y docker-ce-cli

# Configure git for the demo user
RUN git config --global user.email "demo@example.com" && \
    git config --global user.name "Demo User" && \
    git config --global init.defaultBranch main

# Set up a nice shell environment with eza and other aliases
RUN { \
        echo ''; \
        echo '# eza aliases'; \
        echo 'alias ls="eza"'; \
        echo 'alias l="eza -l"'; \
        echo 'alias ll="eza -la --icons"'; \
        echo ''; \
        echo '# bat alias on debian'; \
        echo 'alias bat="batcat"'; \
        echo ''; \
        echo '# Other aliases'; \
        echo 'alias v="nvim"'; \
        echo 'alias y="yazi"'; \
        echo 'alias c="clear"'; \
    } >> /root/.bashrc

# Set the working directory
WORKDIR /app

# Upgrade pip and install uv
RUN pip install --upgrade pip && pip install uv

# Copy all the demo code into the container
COPY . .

# Set the entrypoint to keep the container running if needed for interactive use
CMD ["tail", "-f", "/dev/null"]
