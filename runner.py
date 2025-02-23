import logging
from orpheus.config import init_configs
import os
import sys
import click


log = logging.getLogger(__name__)

class RunTargets:
    SERVER = 'server'
    CELERY_WORKER = 'celery_worker'
    CELERY_BEAT = 'celery_beat'
    IPYTHON = 'ipython'


class InvalidStartParams(Exception):
    pass


@click.group()
def cli():
    """Run different parts of the application."""


def run_celery_worker(queues: str | None = None) -> None:
    from orpheus.services.tasks import run_celery_worker
    run_celery_worker(queues=queues)



def fill_db_test_data():
    """
    temporary func for tests
    :return:
    """
    from orpheus.bl.helpers import get_projects, get_project_files, get_file_content
    from orpheus.bl.indexer import create_index, index_file, delete_index
    from orpheus.index_mappings import repo_index
    delete_index('test_project')

    projects = get_projects()
    project = projects[0]
    files = get_project_files(project)
    create_index(index_name=project.name, index_mapping=repo_index)
    print(project)
    for file_path in files:
        content = get_file_content(file_path)
        print(content)
        index_file(
            repo_name=project.name,
            file_path=file_path,
            content=content,
            index_name=project.name,
        )


def server():
    # fill_db_test_data()
    from orpheus.services.server import run_server
    run_server()


def run_celery_beat():
    from orpheus.services.tasks import run_celery_beat
    run_celery_beat()


def run():
    init_configs()
    if len(sys.argv) != 2:
        raise InvalidStartParams(
            'Run target param should be provided. '
            'Example: python -m billing grpc'
        )

    _, target = sys.argv
    if target == RunTargets.SERVER:
        server()
    elif target == RunTargets.CELERY_WORKER:
        queues = os.environ.get('QUEUES')
        run_celery_worker(
            queues=queues,
        )
    elif target == RunTargets.CELERY_BEAT:
        run_celery_beat()
    else:
        raise ValueError('Invalid target to run: %s' % target)


if __name__ == '__main__':
    run()
