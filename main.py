import sys

import click
from ruamel.yaml import YAML

from yaml_patch import patch


@click.command(
    help="""
Applies patches to a yaml string, keeping most of the formatting and comments.

\b
Some formatting is not kept due to underlying yaml library limitations:
  - Indentation will be forced to two spaces
  - Spacing before sequence dashes will be forced to two spaces
  - Empty lines at the start of the string will be removed

You can pass any number of patches to be applied, they use the following syntax options:

\b
Patch a single value:
  <field>.<subfield>=<value>
Example:
  spec.replicas=2

\b
Patch a value inside a single list item:
  <field>.[<position]>.<subfield>=<value>
Example:
  spec.template.containers.[0].image="mycontainer:latest"

\b
Patch a value inside all list items:
  <field>.[].<subfield>=<value>
Example:
  spec.template.containers.[].image="mycontainer:latest"

\b
When calling this tool from a command line, it's higly recommended that you quote all patches arguments to avoid terminal issues.
Example:
  yaml-patch -f test.yml 'spec.template.containers.[0].image="mycontainer:latest"'
""",
)
@click.option(
    "--file", "-f", type=click.File("r"), default=sys.stdin, help="Path to yaml file being patched. Defaults to stdin."
)
@click.option(
    "--output", "-o", type=click.File("w"), default=sys.stdout, help="Path to output patched file. Defaults to stdout."
)
@click.argument("patches", nargs=-1)
def cli(file, output, patches):
    # Split each patch into key+value separated by `=`. Use YAML to load the values coming from command line to ensure
    # they are parsed into yaml syntax equivalents (automatically detect strings, ints, bools, etc).
    yaml = YAML()
    dict_patches = dict()
    for p in patches:
        k, v = p.split("=")
        dict_patches[k] = yaml.load(v)

    patched = patch(file.read(), dict_patches)
    output.write(patched)


if __name__ == "__main__":
    cli()
