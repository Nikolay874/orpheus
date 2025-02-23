import os
from orpheus.config import get_config
from orpheus.types import Project
from os import listdir
from os.path import isfile, join

config = get_config()


def get_project_files(project: Project) -> list:
    path_ = project.path
    onlyfiles = [join(path_, f) for f in listdir(path_) if
                 isfile(join(path_, f))]
    return onlyfiles


def get_projects() -> list[Project]:
    root = config.storage_name
    projects = []
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)):
            projects.append(
                Project(
                    path=os.path.join(root, item),
                    name=item
                )
            )
    return projects


def get_file_content(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()
