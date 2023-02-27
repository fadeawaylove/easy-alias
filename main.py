import json
import os

import click

HOME = os.path.expanduser('~')


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


command_config_handler = ConfigHandler("commands.json")


@click.group()
def cli():
    pass


@click.command(name="list")
def list_():
    """show alias command list"""
    data = command_config_handler.get_all() or {}
    click.echo("commands list:")
    for k, v in data.items():
        click.echo(f"  k\t{v}")


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


@click.command(name="add")
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
    click.echo(f"ok! use like this:")
    click.secho(f"  pee {name}", fg="green")


cli.add_command(list_)
cli.add_command(add_)
cli.add_command(test_)


@click.command()
@click.argument("name")
def pae(name):
    """execute command which you already added"""
    cmd_str = command_config_handler.get(name)
    if not cmd_str:
        return click.secho(f"alias name {name} represents no command!")
    try:
        os.system(cmd_str)
    except Exception as e:
        click.echo(f"execute failed, error msg is below:")
        click.secho(e, fg='red')


if __name__ == '__main__':
    cli()
