#! /usr/bin/env python3

import subprocess
import sys

__author__ = 'Guillaume Legrand'

UNINSTALL_APP_PREFIXES = ['com.example']

CMD_ADB_NAME = 'adb'
CMD_ADB_DEVICE_ARG_PREFIX = '-s'
CMD_ADB_SHELL_COMMAND = ['shell', 'pm list packages -3 -f']
CMD_ADB_UNINSTALL_COMMAND = ['uninstall']


def adb_uninstall(device, package):
    uninstallPackageCmd = [CMD_ADB_NAME] + ([CMD_ADB_DEVICE_ARG_PREFIX, device] if device else []) + CMD_ADB_UNINSTALL_COMMAND

    subprocess.check_call(uninstallPackageCmd + [package])


def adb_list_packages(device):
    listPackagesCmd = [CMD_ADB_NAME] + ([CMD_ADB_DEVICE_ARG_PREFIX, device] if device else []) + CMD_ADB_SHELL_COMMAND
    return subprocess.check_output(listPackagesCmd)


def get_package_adb(package_line):
    _, suffix = package_line.split('=')
    return suffix


def uninstall(device, app_prefixes):
    installed_packages = ''
    try:
        retrieved_packages = adb_list_packages(device)
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
            adb_uninstall(device, package)
            print("uninstalled: " + package)
        except subprocess.CalledProcessError as calledProcessError:
            print("Failed execute adb to uninstall package '" + package + "'", calledProcessError, file=sys.stderr)


def get_device_argument():
    # no need for argparse yet
    args = sys.argv
    return args[1] if len(args) >= 2 else None


if __name__ == '__main__':
    uninstall(get_device_argument(), UNINSTALL_APP_PREFIXES)
