#!/usr/bin/env python3
import requests
import json
import datetime
import os

def get_latest_release(repo:str):
    """Get the latest release from a GitHub repository."""
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch latest release: {response.status_code} {response.text}")
    info = response.json()
    return info["tag_name"], info["body"], info["html_url"]

def update_changelog(root_dir:str, release:str, body:str, pkg_name:str):
    lines = []
    if os.path.exists(f"{root_dir}/debian/changelog"):
        with open(f"{root_dir}/debian/changelog", "r") as f:
            lines = f.readlines()

        old_release = lines[0].split()[1][1:-1]
        if old_release == release:
            return

    with open(f"{root_dir}/debian/changelog", "w") as f:
        f.write(f'{pkg_name} ({release}) unstable; urgency=medium\n')
        f.write("\n")
        for line in body.splitlines():
            sline = line.strip()
            if sline and sline[0] in ['*', '+', '-']:
                f.write(f"  * {sline[1:].strip()}\n")
        f.write(f"\n -- machsix <28209092+machsix@users.noreply.github.com> {datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}\n")
        if lines:
            f.write("\n")
            f.write('\n'.join(lines))

def update_control(root_dir:str, release:str):
    """Update the control file with the new version."""
    with open(f"{root_dir}/debian/control", "r") as f:
        lines = f.readlines()
    with open(f"{root_dir}/debian/control", "w") as f:
        for line in lines:
            if line.startswith("Standards-Version:"):
                f.write(f"Standards-Version: {release}\n")
            else:
                f.write(line)

def write_release_note(root_dir:str, release:str, pkg_name:str, permalink:str):
    with open(f"{root_dir}/release.txt", "w") as f:
        f.write(f"**{pkg_name} ({release})**\n")
        f.write(f"UpstreamURL: {permalink}\n")

if __name__ == '__main__':
    # Define the repository and package name
    upstream_repo = "fairyglade/ly"
    pkg_name = "ly"

    # Get the latest release information
    release, body, permalink = get_latest_release(upstream_repo)
    if release.startswith("v"):
        release = release[1:]

    # Write the changelog
    update_changelog(".", release, body, pkg_name)

    # Update the control file
    update_control(".", release)

    write_release_note(".", release, pkg_name, permalink)

    print(release)

