import os
import typer
from rich import print
from go_project_cli.examples.example import example_file_txt


class Semantic:
    # It needs to be modified to suit the team convention.
    def __init__(self, semantic: str):
        semantics: dict[str, str] = dict(
            controller='controllers',
            co='controllers',
            service='services',
            s='services',
            repository='repositories',
            r='repositories',
            model='models',
            m='models'
        )
        self.folder_name = semantics.get(semantic)
        self.file_name = semantics.get(semantic)[:-1] \
            if not (semantic == 'r' or semantic == 'repository') else 'repository'

    def get_folder_name(self) -> str | None:
        return self.folder_name

    def get_file_name(self) -> str | None:
        return self.file_name


def generate_file(semantic: str, package_name: str, path: str = ''):
    if semantic not in ['controller', 'co', 'service', 's', 'repository', 'r', 'model', 'm']:
        print(f'semantic {semantic} not found')
        raise typer.Exit(1)

    sem = Semantic(semantic)
    folder_name = sem.folder_name
    file_name = sem.file_name

    try:
        # Create the folder if it doesn't exist
        folder_name = os.path.join(path, folder_name)
        dir_exists = os.path.exists(folder_name)
        if dir_exists:
            print('Nothing to be done.')
            raise typer.Exit(1)
        os.makedirs(folder_name, exist_ok=True)

        # Create the Golang file with the same name as the folder
        go_file_name = os.path.join(folder_name, file_name + ".go")

        go_code = example_file_txt.format(package_name=package_name)

        with open(go_file_name, 'w') as go_file:
            go_file.write(go_code)

        print(f"Golang folder '{folder_name}' and file '{go_file_name}' created successfully.")
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(1)


def new_package(package_name):
    try:
        os.makedirs(package_name, exist_ok=True)
        semantics = ['co', 's', 'r', 'm']
        for semantic in semantics:
            generate_file(semantic, package_name, package_name)
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(1)
