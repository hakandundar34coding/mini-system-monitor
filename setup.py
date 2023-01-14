#!/usr/bin/env python3

from setuptools import setup, find_packages, os
import sys
import shutil


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

    shutil.copy2("mini-system-monitor.png", "io.github.hakandundar34coding.mini-system-monitor.png")

    with open("io.github.hakandundar34coding.mini-system-monitor.desktop") as reader:
        desktop_file_content = reader.read()
    desktop_file_content = desktop_file_content.replace("Icon=mini-system-monitor", "Icon=io.github.hakandundar34coding.mini-system-monitor")
    with open("io.github.hakandundar34coding.mini-system-monitor.desktop", "w") as writer:
        writer.write(desktop_file_content)

    with open("mini-system-monitor") as reader:
        script_file_content = reader.read()
    script_file_content = script_file_content.replace("/usr/share/mini-system-monitor/src/", "/app/share/mini-system-monitor/src/")
    script_file_content = script_file_content.replace("#!/usr/bin/env python3", "#!/usr/bin/python3")
    with open("mini-system-monitor", "w") as writer:
        writer.write(script_file_content)

    data_files = [
        ("/app/share/applications/", ["io.github.hakandundar34coding.mini-system-monitor.desktop"]),
        ("/app/share/icons/128x128/scalable/apps/", ["io.github.hakandundar34coding.mini-system-monitor.png"]),
        ("/app/share/mini-system-monitor/", ["mini-system-monitor.png"]),
        ("/app/share/mini-system-monitor/src/", ["Main.py"]),
        ("/app/share/appdata/", ["io.github.hakandundar34coding.mini-system-monitor.appdata.xml"]),
        ("/app/bin/", ["mini-system-monitor"])
    ]


if PREFIX != "/app":

    os.chmod("io.github.hakandundar34coding.mini-system-monitor.desktop", 0o644)
    os.chmod("Main.py", 0o644)
    os.chmod("mini-system-monitor.png", 0o644)

    shutil.copy2("mini-system-monitor.png", "io.github.hakandundar34coding.mini-system-monitor.png")

    with open("io.github.hakandundar34coding.mini-system-monitor.desktop") as reader:
        desktop_file_content = reader.read()
    desktop_file_content = desktop_file_content.replace("Icon=mini-system-monitor", "Icon=io.github.hakandundar34coding.mini-system-monitor")
    with open("io.github.hakandundar34coding.mini-system-monitor.desktop", "w") as writer:
        writer.write(desktop_file_content)

    data_files = [
        ("/usr/share/applications/", ["io.github.hakandundar34coding.mini-system-monitor.desktop"]),
        ("/usr/share/icons/128x128/scalable/apps/", ["io.github.hakandundar34coding.mini-system-monitor.png"]),
        ("/usr/share/mini-system-monitor/", ["mini-system-monitor.png"]),
        ("/usr/share/mini-system-monitor/src/", ["Main.py"]),
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
