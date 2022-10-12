#!/usr/bin/env python3
from setuptools import setup, find_packages, os
import sys


with open(os.path.dirname(os.path.realpath(__file__)) + "/src/__version__") as reader:
    version = reader.read().strip()


def files_in_folder(folder):
    file_paths = []
    for file in [filename for filename in os.listdir(folder)]:
        file_paths.append(folder + file)
    return file_paths


PREFIX = "/usr"
if "--flatpak" in sys.argv:
    PREFIX = "/app"
    sys.argv.remove("--flatpak")


if PREFIX == "/app":
    os.rename("icons/mini-system-monitor.svg", "icons/apps/com.github.hakandundar34coding.mini-system-monitor.svg")

    with open("integration/com.github.hakandundar34coding.mini-system-monitor.desktop") as reader:
        desktop_file_content = reader.read()
    desktop_file_content = desktop_file_content.replace("Icon=mini-system-monitor", "Icon=com.github.hakandundar34coding.mini-system-monitor")
    with open("integration/com.github.hakandundar34coding.mini-system-monitor.desktop", "w") as writer:
        writer.write(desktop_file_content)

    with open("integration/mini-system-monitor") as reader:
        script_file_content = reader.read()
    script_file_content = script_file_content.replace("/usr", "/app")
    with open("integration/mini-system-monitor", "w") as writer:
        writer.write(script_file_content)

    data_files = [
        ("/app/share/applications/", ["integration/com.github.hakandundar34coding.mini-system-monitor.desktop"]),
        ("/app/share/mini-system-monitor/src/", files_in_folder("src/")),
        ("/usr/share/icons/hicolor/scalable/apps/", ["icons/com.github.hakandundar34coding.mini-system-monitor.svg"]),
        ("/app/share/mini-system-monitor/icons/", ["icons/mini-system-monitor.png"]),
        ("/app/share/mini-system-monitor/images/", ["images/smc_screenshot1.png"]),
        ("/app/bin/", ["integration/mini-system-monitor"])
    ]


setup(
    name="mini-system-monitor",
    version=version,
    description="Mini version of 'System Monitoring Center'.",
    long_description="Provides information about CPU, RAM, Disk, Network usage.",
    author="Hakan Dündar",
    author_email="hakandundar34coding@gmail.com",
    url="https://github.com/hakandundar34coding/mini-system-monitor",
    keywords="system monitor task manager performance cpu ram swap memory disk network",
    license="GPLv3",
    install_requires=["PyGObject"],
    python_requires=">=3.6",
    packages=find_packages(),
    data_files=data_files,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Monitoring",
    ],
)
