"""
本地安装测试
pip install -e .
"""

import json
import os
import sys
import click

HOME = os.path.expanduser('~')
COMMAND_PATH = os.path.dirname(sys.executable)
PLATFORM = sys.platform


class ConfigHandler:
    dir_name = ".easy_alias"
    config_dir = os.path.join(HOME, dir_name)
    os.makedirs(config_dir, exist_ok=True)

    def __init__(self, name):
        self.config_file = os.path.join(self.config_dir, name)
        self._init_file()

    def _init_file(self):
        if not os.path.exists(self.config_file):
            open(self.config_file, "w").write("{}")

    def set(self, k, v):
        json.dump({**self.get_all(), k: v}, open(self.config_file, "w"))

    def get(self, k):
        return json.load(open(self.config_file, "r")).get(k)

    def get_all(self):
        return json.load(open(self.config_file, "r"))

    def delete_all(self):
        json.dump({}, open(self.config_file, "w"))

    def delete_one(self, name):
        data = self.get_all()
        if name in data:
            cmd = data.pop(name)
            json.dump(data, open(self.config_file, "w"))
            return cmd


command_config_handler = ConfigHandler("commands.json")


def add_sh(name, check_exists=True):
    file = os.path.join(COMMAND_PATH, f"{name}.bat")
    if check_exists:
        verify_file_list = [
            os.path.join(COMMAND_PATH, f"{name}.bat"),
            os.path.join(COMMAND_PATH, f"{name}.exe"),
            os.path.join(COMMAND_PATH, f"{name}"),
        ]
        for vf in verify_file_list:
            if os.path.exists(vf):
                return False, f"command already exists, at path {vf}"

    if PLATFORM == "win32":
        exec_str = f"""
            @echo off
            _pea_exec {name} %*
            """
    elif PLATFORM in ("linux", "darwin"):
        exec_str = f"""
            # !/bin/bash
            _pea_exec {name}
            """
    else:
        msg = f"not supported platform {PLATFORM}"
        return False, msg
    open(file, "w").write(exec_str)
    return True, "ok"


def remove_sh(name):
    file = os.path.join(COMMAND_PATH, f"{name}.bat")
    try:
        os.remove(file)
    except Exception as e:
        click.secho(f"error deleting 【{name}】, {e}", fg="yellow")


@click.group()
def cli():
    pass


@click.command(name="list")
def list_():
    """show alias command list"""
    data = command_config_handler.get_all() or {}
    click.echo("commands list:")
    for k, v in data.items():
        click.echo(f"  {k}\t{v}")


@click.command(name="test")
@click.argument("cmd_tuple", nargs=-1)
def test_(cmd_tuple):
    """test alias command"""
    if not cmd_tuple:
        return click.secho("command can't be null", fg="red")
    cmd_str = " ".join(cmd_tuple)
    try:
        os.system(cmd_str)
    except Exception as e:
        click.echo(f"execute failed, error msg is below:")
        click.secho(e, fg='red')


@click.command(name="add",
               context_settings=dict(
                   ignore_unknown_options=True,
                   allow_extra_args=True,
               ))
@click.argument("name")
@click.argument("cmd_tuple", nargs=-1)
def add_(name, cmd_tuple):
    """add new alias command"""
    if not cmd_tuple:
        return click.secho("command can't be null", fg="red")
    old_cmd = command_config_handler.get(name)
    if old_cmd:
        click.secho(f"[{name}] already exists for a command [{old_cmd}]", fg="yellow")
        click.confirm("continue? ", abort=True)

    cmd_str = " ".join(cmd_tuple)

    command_config_handler.set(name, cmd_str)
    ok, msg = add_sh(name, check_exists=False if old_cmd else True)
    if not ok:
        command_config_handler.delete_one(name)
        return click.secho(f"add failed, {msg}", fg="red")

    click.secho(f"ok, now you can just enter 【{name}】 in terminal.", fg="green")


@click.command(name="del")
@click.option("--name", "-n", help="delete a certain command alise!")
@click.option("--all", "-a", "all_", help="delete all command aliases!",
              show_default=True,
              type=bool,
              default=False
              )
def del_(name, all_):
    """delete command alis"""
    if all_:
        click.confirm("Delete all command aliases?", abort=True)
        all_commands = command_config_handler.get_all()
        command_config_handler.delete_all()
        for c in all_commands:
            remove_sh(c)
        return click.secho(f"delete all command success!", fg="green")
    if not name:
        return click.secho("please specify a alias name!", fg="yellow")
    cmd = command_config_handler.delete_one(name)
    if cmd:
        click.secho(f"delete {name} success, command is {cmd}", fg="green")
        remove_sh(name)
    else:
        click.secho(f"no command for alias {name}", fg="yellow")


cli.add_command(list_)
cli.add_command(add_)
cli.add_command(test_)
cli.add_command(del_)


@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument("name")
@click.argument("params", nargs=-1)
def pae(name, params):
    """execute command which you already added"""
    cmd_str = command_config_handler.get(name)
    if not cmd_str:
        return click.secho(f"{name} represents no command!", fg="yellow")
    try:
        if params:
            cmd_str = cmd_str + " " + " ".join(params)
        click.secho(f"{cmd_str}", fg="black", bg="white")
        os.system(cmd_str)
    except Exception as e:
        click.echo(f"execute failed, error msg is below:")
        click.secho(e, fg='red')
