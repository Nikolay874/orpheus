import gitlab

from orpheus.config import get_config


config = get_config()


gl = gitlab.Gitlab(
    url='https://gitlab.evo.dev/',
    private_token=config.gitlab_token
)