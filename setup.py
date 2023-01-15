#!/usr/bin/env python3

from setuptools import setup, find_packages, os
import sys


with open(os.path.dirname(os.path.realpath(__file__)) + "/mini-system-monitor") as reader:
    file_content_lines = reader.read().strip().split("\n")

for line in file_content_lines:
    if line.startswith("SOFTWARE_VERSION") == True:
        version = line.split("=")[1].strip(' "')


PREFIX = "/usr"
if "--flatpak" in sys.argv:
    PREFIX = "/app"
    sys.argv.remove("--flatpak")


if PREFIX == "/app":

    os.rename("mini-system-monitor.png", "io.github.hakandundar34coding.mini-system-monitor.png")

    with open("io.github.hakandundar34coding.mini-system-monitor.desktop") as reader:
        desktop_file_content = reader.read()
    desktop_file_content = desktop_file_content.replace("Icon=mini-system-monitor", "Icon=io.github.hakandundar34coding.mini-system-monitor")
    with open("io.github.hakandundar34coding.mini-system-monitor.desktop", "w") as writer:
        writer.write(desktop_file_content)

    with open("mini-system-monitor") as reader:
        script_file_content = reader.read()
    script_file_content = script_file_content.replace("#!/usr/bin/env python3", "#!/usr/bin/python3")
    with open("mini-system-monitor", "w") as writer:
        writer.write(script_file_content)

    data_files = [
        ("/app/share/applications/", ["io.github.hakandundar34coding.mini-system-monitor.desktop"]),
        ("/app/share/icons/hicolor/128x128/apps/", ["io.github.hakandundar34coding.mini-system-monitor.png"]),
        ("/app/share/appdata/", ["io.github.hakandundar34coding.mini-system-monitor.appdata.xml"]),
        ("/app/bin/", ["mini-system-monitor"])
    ]


if PREFIX != "/app":

    os.chmod("io.github.hakandundar34coding.mini-system-monitor.desktop", 0o644)

    data_files = [
        ("/usr/share/applications/", ["io.github.hakandundar34coding.mini-system-monitor.desktop"]),
        ("/usr/share/icons/hicolor/128x128/apps/", ["mini-system-monitor.png"]),
        ("/usr/bin/", ["mini-system-monitor"])
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
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Monitoring",
    ],
)
