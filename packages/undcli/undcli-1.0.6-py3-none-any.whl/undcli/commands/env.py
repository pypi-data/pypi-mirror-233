import typer
import json
from enum import Enum
import undcli.utils as utils
import os

app = typer.Typer()

class MLFramework(str, Enum):
    tensorflow = "tensorflow"
    pytorch = "pytorch"
    jax = "jax"
    scikit_learn = "scikit-learn"
    keras = "keras"

@app.command(help="Create a new python environment.")
def create(name: str):
    # Create a new environment, ask the user the cuda version they want to use, the python version and the ml framework they want to use

    # Check if the environment already exists
    with open("config.json", "r") as f:
        config_file = json.loads(f.read())
        for env in config_file["environments"]:
            if(env["name"] == name):
                typer.echo("Environment already exists.")
                return
            
    # Ask the user the cuda version they want to use
    cuda_version = typer.prompt("CUDA version", default="11.4")
    # Ask the user the python version they want to use
    python_version = typer.prompt("Python version", default="3.8.10")
    # Ask the user the ml framework they want to use
    ml_framework = typer.prompt("ML framework", default=MLFramework.tensorflow, type=MLFramework, show_choices=True)
    # Save the environment in config.json
    config = {
        "name": name,
        "cuda_version": cuda_version,
        "python_version": python_version,
        "ml_framework": ml_framework
    }
    
    # Install pyenv if it's not installed    
    if(not os.path.exists(os.path.expanduser("~/.pyenv"))):  
        typer.echo("Pyenv not installed. Run again after installing pyenv.")
        return

    typer.echo("Installing python version. This may take a while.")
    # Install python version using pyenv
    utils.run_command(f"pyenv install {python_version}")
    # Create python env using pyenv
    utils.run_command(f"pyenv virtualenv {python_version} {name}")
    # Install ml framework
    utils.run_command(f"pyenv activate {name}")
    # Install jupyter
    utils.run_command("pip install jupyter")
    # Install jupyterlab
    utils.run_command("pip install jupyterlab")
    # Install tqdm
    utils.run_command("pip install tqdm")

    # Set the default environment in the project if it's the first environment
    if(len(config_file["environments"]) == 0):
        config_file["environments"].append(config)
        config_file["default_environment"] = name
      
    with open("config.json", "w") as f:
        f.write(json.dumps(config_file, indent=2))
    typer.echo("Created environment. Please install your ml framework of choice.")

@app.command(help="Use an existing python environment.")
def use(name: str):
    # Check if the environment exists
    with open("config.json", "r") as f:
        config_file = json.loads(f.read())
        for env in config_file["environments"]:
            if(env["name"] == name):
                # Activate the environment
                utils.run_command(f"pyenv activate {name}")
                return
    typer.echo("Environment does not exist.")

@app.command(help="Set the default python environment.", name="set")
def default(name: str):
    # Check if the environment exists
    with open("config.json", "r") as f:
        config_file = json.loads(f.read())
        for env in config_file["environments"]:
            if(env["name"] == name):
                # Set the default environment in the project
                config_file["default_environment"] = name
                with open("config.json", "w") as f:
                    f.write(json.dumps(config_file, indent=2))
                return
          
@app.command(help="Use the default python environment for the project.")
def load(): 
    # Get and set the default environment of the project
    with open("config.json", "r") as f:
        config_file = json.loads(f.read())
        if("default_environment" in config_file):
            default_name = config_file["default_environment"]
            utils.run_command(f"pyenv activate {default_name}")
        else:
            typer.echo("No default environment set.")

@app.command(help="Freeze the requirements of the current environment.")
def freeze():
    # Freeze the requirements of the current environment
    utils.run_command("pip freeze > requirements.txt")

@app.command(help="Install the requirements of the current environment.")
def install():
    # Install the requirements of the current environment
    utils.run_command("pip install -r requirements.txt")


if __name__ == "__main__":
    app()