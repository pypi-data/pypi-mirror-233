# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2019 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2
"""TODO"""

import click

from apio.managers.scons import SCons


# R0913: Too many arguments (6/5)
# pylint: disable=R0913
# pylint: disable=W0622
@click.command("time")
@click.pass_context
@click.option(
    "-b", "--board", type=str, metavar="board", help="Set the board."
)
@click.option("--fpga", type=str, metavar="fpga", help="Set the FPGA.")
@click.option(
    "--size", type=str, metavar="size", help="Set the FPGA type (1k/8k)."
)
@click.option(
    "--type", type=str, metavar="type", help="Set the FPGA type (hx/lp)."
)
@click.option(
    "--pack", type=str, metavar="package", help="Set the FPGA package."
)
@click.option(
    "-p",
    "--project-dir",
    type=str,
    metavar="path",
    help="Set the target directory for the project.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Show the entire output of the command.",
)
@click.option(
    "--verbose-yosys",
    is_flag=True,
    help="Show the yosys output of the command.",
)
@click.option(
    "--verbose-pnr", is_flag=True, help="Show the pnr output of the command."
)
def cli(
    ctx,
    board,
    fpga,
    pack,
    type,
    size,
    project_dir,
    verbose,
    verbose_yosys,
    verbose_pnr,
):
    """Bitstream timing analysis."""

    # Run scons
    exit_code = SCons(project_dir).time(
        {
            "board": board,
            "fpga": fpga,
            "size": size,
            "type": type,
            "pack": pack,
            "verbose": {
                "all": verbose,
                "yosys": verbose_yosys,
                "pnr": verbose_pnr,
            },
        }
    )
    ctx.exit(exit_code)
