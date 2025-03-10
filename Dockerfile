# Use the official Debian base image
FROM debian:bookworm

# Set the maintainer label
LABEL maintainer="your-email@example.com"

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies and tools
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    devscripts \
    dh-make \
    wget \
    libpam0g-dev \
    libxcb-xkb-dev \
    curl \
    sudo \
    gnupg \
    lsb-release \
    && apt-get clean

WORKDIR /data

COPY . .
CMD make -f Makefile_deb
