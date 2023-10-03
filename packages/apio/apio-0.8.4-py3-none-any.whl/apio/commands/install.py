"""DOC: TODO"""
# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2019 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import click

from apio.managers.installer import Installer
from apio.resources import Resources

# R0801: Similar lines in 2 files
# pylint: disable=R0801
platforms = [
    "linux",
    "linux_x86_64",
    "linux_i686",
    "linux_armv7l",
    "linux_aarch64",
    "windows",
    "windows_x86",
    "windows_amd64",
    "darwin",
]


# R0913: Too many arguments (6/5)
# pylint: disable=R0913
# pylint: disable=W0622
@click.command("install")
@click.pass_context
@click.argument("packages", nargs=-1)
@click.option("-a", "--all", is_flag=True, help="Install all packages.")
@click.option(
    "-l", "--list", is_flag=True, help="List all available packages."
)
@click.option(
    "-f", "--force", is_flag=True, help="Force the packages installation."
)
@click.option(
    "-p",
    "--platform",
    type=click.Choice(platforms),
    metavar="",
    help=f"Set the platform [{', '.join(platforms)}] (Advanced).",
)
def cli(ctx, packages, all, list, force, platform):
    """Install packages.
    Input parameters:
      - packages: List with the names of the packages to install
      - all: Flag: Install all the packages available for that platform
      - list: Flag. List all the packages (installed or not)
      - force: Flag. Force installation
      - platform: Flag. Select platform (advaced. For developers)
    """

    # -- Install the given packages
    if packages:
        for package in packages:
            # -- The instalation is performed by the Installer object
            inst = Installer(package, platform, force)

            inst.install()

    # -- Install all the available packages
    elif all:  # pragma: no cover
        # -- Get all the resources
        resources = Resources(platform)

        # -- Get all the packages
        packages = resources.packages

        # -- Install all the packages... except the obolete one
        for package in packages:
            # -- do NOT install the obsolete packages
            if package not in resources.obsolete_pkgs:
                Installer(package, platform, force).install()

    # -- List all the packages (installed or not)
    elif list:
        # -- Get all the resources
        resources = Resources(platform)

        # -- List the packages
        resources.list_packages()

    # -- Invalid option. Just show the help
    else:
        click.secho(ctx.get_help())
