import typer

from go_project_cli import utils
from typing_extensions import Annotated

app = typer.Typer(help='Golang Project Folder and File Creation CLI')


@app.command()
def new(package_name: Annotated[str, typer.Argument(
    help='Name of the package from which Controller, Service, Model, Repository was created'
)]):
    """
    Create package with Controller, Service, Model, Repository
    """
    utils.new_package(package_name)


@app.command()
def generate(semantic: Annotated[str, typer.Argument(help='Semantic name to create')],
             package_name: Annotated[str, typer.Argument(help='Name of package to which Semantic belongs')]):
    """
    Create semantic folders and files such as controllers, services, and models
    """
    utils.generate_file(semantic, package_name)


if __name__ == '__main__':
    app()
