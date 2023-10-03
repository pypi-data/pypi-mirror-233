import typer

from go_project_cli import utils

app = typer.Typer()


@app.command()
def new(package_name: str):
    """
    Create a new Pacakge With Controller, Service, Model, Repository Folder
    """
    utils.new_package(package_name)


@app.command()
def generate(semantic: str, package_name: str):
    """
    Generate folders and files
    """
    utils.generate_file(semantic, package_name)


if __name__ == '__main__':
    app()
