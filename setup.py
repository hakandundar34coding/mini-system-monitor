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

    os.rename("icons/mini-system-monitor.svg", "icons/io.github.hakandundar34coding.mini-system-monitor.svg")
    os.rename("integration/com.github.hakandundar34coding.mini-system-monitor.desktop", "integration/io.github.hakandundar34coding.mini-system-monitor.desktop")

    with open("integration/io.github.hakandundar34coding.mini-system-monitor.desktop") as reader:
        desktop_file_content = reader.read()
    desktop_file_content = desktop_file_content.replace("Icon=mini-system-monitor", "Icon=io.github.hakandundar34coding.mini-system-monitor")
    with open("integration/io.github.hakandundar34coding.mini-system-monitor.desktop", "w") as writer:
        writer.write(desktop_file_content)

    with open("integration/mini-system-monitor") as reader:
        script_file_content = reader.read()
    script_file_content = script_file_content.replace("/usr/share/mini-system-monitor/src/", "/app/share/mini-system-monitor/src/")
    with open("integration/mini-system-monitor", "w") as writer:
        writer.write(script_file_content)

    data_files = [
        ("/app/share/applications/", ["integration/io.github.hakandundar34coding.mini-system-monitor.desktop"]),
        ("/app/share/icons/hicolor/scalable/apps/", ["icons/io.github.hakandundar34coding.mini-system-monitor.svg"]),
        ("/app/share/mini-system-monitor/src/", files_in_folder("src/")),
        ("/app/share/mini-system-monitor/icons/", ["icons/mini-system-monitor.png"]),
        ("/app/share/mini-system-monitor/images/", ["images/smc_screenshot1.png"]),
        ("/app/share/appdata/", ["io.github.hakandundar34coding.mini-system-monitor.appdata.xml"]),
        ("/app/bin/", ["integration/mini-system-monitor"])
    ]


if PREFIX != "/app":

    os.chmod("integration/com.github.hakandundar34coding.mini-system-monitor.desktop", 0o644)
    for file in files_in_folder("src/"):
        os.chmod(file, 0o644)
    for file in files_in_folder("icons/"):
        os.chmod(file, 0o644)
    os.chmod("icons/mini-system-monitor.svg", 0o644)
    os.chmod("icons/mini-system-monitor.png", 0o644)
    os.chmod("images/smc_screenshot1.png", 0o644)

    data_files = [
        ("/usr/share/applications/", ["integration/com.github.hakandundar34coding.mini-system-monitor.desktop"]),
        ("/usr/share/icons/hicolor/scalable/apps/", ["icons/mini-system-monitor.svg"]),
        ("/usr/share/mini-system-monitor/src/", files_in_folder("src/")),
        ("/usr/share/mini-system-monitor/icons/", ["icons/mini-system-monitor.png"]),
        ("/usr/share/mini-system-monitor/images/", ["images/smc_screenshot1.png"]),
        ("/usr/bin/", ["integration/mini-system-monitor"])
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
