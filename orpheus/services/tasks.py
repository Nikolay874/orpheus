import os
from pathlib import Path
import subprocess
import logging
from datetime import timedelta
import re
from urllib.parse import urlparse

from celery import Celery
from celery.schedules import crontab  # type: ignore
from celery.signals import task_postrun, setup_logging  # type: ignore

from orpheus.bl.helpers import get_projects, get_project_files, get_file_content
from orpheus.bl.indexer import create_index, index_file
from orpheus.config import get_config
from orpheus.index_mappings import repo_index

INCLUDE = [
     "orpheus.bl.repository"
]
POOL = 'solo'

REPO_QUEUE = 'repo'
GENERAL_QUEUE = 'general'
CELERY_RESULT_EXPIRES = 60

log = logging.getLogger(__name__)
config = get_config()

celery_app: Celery = Celery(
    broker=config.celery_broker_url,
    include=INCLUDE,
    loglevel=config.loglevel,
    result_expires=CELERY_RESULT_EXPIRES,
)

def get_repository_name(repo_url: str) -> str:
    """
    Отримує назву репозиторію з URL.

    :param repo_url: URL-адреса репозиторію (наприклад, https://gitlab.com/user/project.git)
    :return: Назва репозиторію (наприклад, project)
    """
    parsed_url = urlparse(repo_url)
    repo_name = parsed_url.path.strip("/").split("/")[-1]  # Отримуємо останню частину шляху

    # Видаляємо суфікс .git, якщо він є
    return re.sub(r"\.git$", "", repo_name)


@celery_app.task
def load_repo():
    """Задача для періодичного завантаження репозиторіїв."""
    log.info("Запуск таски завантаження репозиторіїв")
    REPO_BASE_DIR = config.REPO_BASE_DIR
    for repo_url in config.repositories_url:
        repo_name = get_repository_name(repo_url)
        repo_path = os.path.join(REPO_BASE_DIR, repo_name)
        if repo_path.exists():
            log.info(f"Оновлення репозиторію: {repo_name}")
            result = subprocess.run(["git", "-C", str(repo_path), "pull"],
                                    capture_output=True, text=True)
        else:
            log.info(f"Клонування репозиторію: {repo_name}")
            result = subprocess.run(["git", "clone", repo_url, str(repo_path)],
                                    capture_output=True, text=True)
        if result.returncode != 0:
            log.error(f"Помилка при обробці {repo_name}: {result.stderr}")
            continue
        log.info(f"Репозиторій {repo_name} оновлено.")
        process_repository_files.delay()


@celery_app.task
def process_repository_files():
    projects = get_projects()
    project = projects[0]
    files = get_project_files(project)
    create_index(index_name=project.name, index_mapping=repo_index)
    for file_path in files:
        content = get_file_content(file_path)
        index_file(
            repo_name=project.name,
            file_path=file_path,
            content=content,
            index_name=project.name,
        )

def run_celery_worker(
    queues: str = None,
) -> None:
    log.info('Celery worker is inited(queues=%s)', queues)
    worker = celery_app.Worker(  # type: ignore
        include=INCLUDE,
        loglevel=config.loglevel,
        pool=POOL,
        queues=queues,
    )

    worker.start()


def run_celery_beat():
    beat = celery_app.Beat(
        loglevel=config.loglevel,
        schedule='/var/tmp/celerybeat-schedule',
    )

    beat.run()


celery_app.conf.beat_schedule = {
    'load-repo': {
        'task': 'orpheus.bl.repository.load_repo',
        'schedule': timedelta(seconds=50),
        'options': {'expires': 10},
    },
}
