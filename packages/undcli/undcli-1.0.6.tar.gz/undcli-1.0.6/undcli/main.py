import typer
import os
import json
import undcli.commands.storage as storage
import undcli.commands.env as env
import undcli.utils as utils

app = typer.Typer()
app.add_typer(env.app, name="env")
app.add_typer(storage.app, name="storage")

@app.command(help="Create a new project.")
def create(name: str):
    if(name.count(" ") > 0 or name.count(".") > 0 or name.count("/") > 0 or name.count("\\") > 0):
        typer.echo("Invalid project name: no spaces, dots, slashes, or backslashes allowed.")
        return
    if(os.path.exists(name)):
        typer.echo("Project already exists.")
        return
    os.mkdir(name)
    # Create a json config file
    config = {
        "name": name,
        "version": "0.0.1",
        "description": "A new project.",
        "storages": [],
        "environments": []
    }
    with open(f"{name}/config.json", "w") as f:
        f.write(json.dumps(config, indent=2))
    # Create .gitignore and ignore all the folders inside the storages folder
    with open(f"{name}/.gitignore", "w") as f:
        f.writelines([
          "storages/*", 
          ".venv/*"
        ])
    typer.echo(f"Created project {name}.")
    typer.echo("Run 'cd " + name + "' to enter the project directory.")

@app.command(help="Install recommended version of CUDA.")
def setup_cuda():
    if os.geteuid() != 0:
        print("This script requires superuser privileges. Please run with sudo.")
        exit(1)

    ubuntu_version = utils.get_ubuntu_version()
    if ubuntu_version:
        utils.setup_cuda_ubuntu(ubuntu_version)
    else:
        print("Unable to determine Ubuntu version.")

if __name__ == "__main__":
    app()