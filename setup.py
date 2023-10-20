#!/usr/bin/env python3

from setuptools import setup, find_packages, os
import sys


with open(os.path.dirname(os.path.realpath(__file__)) + "/mini-system-monitor") as reader:
    file_content_lines = reader.read().strip().split("\n")

for line in file_content_lines:
    if line.startswith("SOFTWARE_VERSION") == True:
        version = line.split("=")[1].strip(' "')
        break


PREFIX = "/usr"
if "--flatpak" in sys.argv:
    PREFIX = "/app"
    sys.argv.remove("--flatpak")


data_files = [
    (PREFIX + "/share/applications/", ["io.github.hakandundar34coding.mini-system-monitor.desktop"]),
    (PREFIX + "/share/icons/hicolor/128x128/apps/", ["io.github.hakandundar34coding.mini-system-monitor.png"]),
    (PREFIX + "/share/appdata/", ["io.github.hakandundar34coding.mini-system-monitor.appdata.xml"]),
    (PREFIX + "/bin/", ["mini-system-monitor"])
]


setup(
    name="mini-system-monitor",
    version=version,
    description="Mini version of 'System Monitoring Center'",
    long_description="Provides information about CPU, RAM, Disk, Network usage",
    author="Hakan Dündar",
    author_email="hakandundar34coding@gmail.com",
    url="https://github.com/hakandundar34coding/mini-system-monitor",
    keywords="system monitor task manager performance cpu ram swap memory disk network",
    license="GPLv3",
    python_requires=">=3.6",
    packages=find_packages(),
    data_files=data_files,
)
