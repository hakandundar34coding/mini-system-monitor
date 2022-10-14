#!/bin/sh

flatpak-builder --force-clean build-dir com.github.hakandundar34coding.mini-system-monitor.yml
flatpak-builder --user --install --force-clean build-dir com.github.hakandundar34coding.mini-system-monitor.yml
flatpak run com.github.hakandundar34coding.mini-system-monitor
