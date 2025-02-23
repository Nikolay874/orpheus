import gitlab
import git
from orpheus.services.tasks import celery_app
from orpheus.services.integrations import gl
from orpheus.config import get_config

config = get_config()


@celery_app.task
def load_repo():
    project = gl.projects.get(2286)  # or gl.projects.get(project_id)
    git_url = project.ssh_url_to_repo
