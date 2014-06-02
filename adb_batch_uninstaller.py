#! /usr/bin/env python3

import subprocess
import sys

__author__ = 'Guillaume Legrand'

UNINSTALL_APP_PREFIXES = ['com.example']

CMD_ADB_LIST_PACKAGES = ['adb', 'shell', 'pm list packages -3 -f']


def adb_uninstall(package):
    CMD_ADB_UNINSTALL_PACKAGE = ['adb', 'uninstall']

    subprocess.check_call(CMD_ADB_UNINSTALL_PACKAGE + [package])


def get_package_adb(package_line):
    _, suffix = package_line.split('=')
    return suffix


def uninstall(app_prefixes):
    installed_packages = ''
    try:
        retrieved_packages = subprocess.check_output(CMD_ADB_LIST_PACKAGES)
        installed_packages = (retrieved_packages.decode(sys.stdout.encoding)).splitlines()
        installed_packages = [get_package_adb(line) for line in installed_packages]
    except subprocess.CalledProcessError as calledProcessError:
        print("Failed execute adb to get packages list", calledProcessError, file=sys.stderr)
        return

    packages_to_uninstall = [package for package in installed_packages if
                             any(package.startswith(to_uninstall) for to_uninstall in app_prefixes)]

    print("The following packages will be uninstalled: " + ("\n".join(packages_to_uninstall)) if packages_to_uninstall
          else "No package to uninstall found")

    for package in packages_to_uninstall:
        try:
            adb_uninstall(package)
            print("uninstalled: " + package)
        except subprocess.CalledProcessError as calledProcessError:
            print("Failed execute adb to uninstall package '" + package + "'", calledProcessError, file=sys.stderr)


if __name__ == '__main__':
    uninstall(UNINSTALL_APP_PREFIXES)
