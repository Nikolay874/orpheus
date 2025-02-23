import os
import logging
import trafaret
import yaml
import typing as t
from marshmallow import INCLUDE, Schema, ValidationError, fields
from trafaret import Dict as trDict  # noqa
from trafaret import String as trString  # noqa
from trafaret import Int as trInt  # noqa
from trafaret import List as trList # noqa
from trafaret import Bool as trBool # noqa
from trafaret import DataError
import uvicorn
import os



LOG_FORMAT = (
    'Pid:%(process)d '
    'Functiton:%(name)s '
    'Level:%(levelname)s '
    'Time:%(asctime)s '
    'Message:%(message)s'
)
# uvicorn.config.LOGGING_CONFIG["formatters"]["access"]["fmt"] = LOG_FORMAT
logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.INFO
)

CONFIG_SCHEMA = trDict({
    "version": trString,
    "debug": trBool,
    "celery_broker_url": trString,
    "loglevel": trString,
    "elastic_url": trString,
    "gitlab_token": trString,
    "storage_name": trString,
    "server_host": trString,
    "server_port": trInt,
    "api_server_origins": trList(trString),
    "repositories_url": trList(trString)
})


def validate_config(
        config_dict: t.Dict[str, t.Any],
) -> t.Tuple[t.Optional[str], t.Dict[str, t.Any]]:
    try:
        return None, CONFIG_SCHEMA.check(config_dict)
    except DataError as e:
        return e.as_dict(), {}


class Config(t.NamedTuple):
    debug: bool
    version: str
    celery_broker_url: str
    loglevel: str
    elastic_url: str
    gitlab_token: str
    storage_name: str
    server_host: str
    server_port: int
    api_server_origins: list
    repositories_url: list
    REPO_BASE_DIR: str

    @staticmethod
    def init_from_dict(config_dict: t.Dict[str, t.Any]):
        global config
        print(config_dict)
        config = Config(
            debug=config_dict['debug'],
            version=config_dict['version'],
            celery_broker_url=config_dict['celery_broker_url'],
            loglevel=config_dict['loglevel'],
            elastic_url=config_dict['elastic_url'],
            gitlab_token=config_dict['gitlab_token'],
            storage_name=config_dict['storage_name'],
            server_host=config_dict['server_host'],
            server_port=config_dict['server_port'],
            api_server_origins=config_dict['api_server_origins'],
            repositories_url=config_dict['repositories_url'],
            REPO_BASE_DIR=__name__
        )


class ConfigNotSpecified(Exception):
    pass


class InvalidConfigError(Exception):
    pass


def _merge_configs(a: dict, b: dict):
    merged = {**a}

    for bkey, bval in b.items():
        if isinstance(bval, dict):
            assert isinstance(a[bkey], dict)
            merged[bkey] = _merge_configs(a[bkey], bval)
        else:
            merged[bkey] = bval

    return merged


def read_config(
        config_path: str,
        override_config_path: t.Optional[str],
) -> t.Dict[str, t.Any]:
    if override_config_path:
        with open(override_config_path, 'r') as f:
            override_config_dict = yaml.safe_load(f)
    else:
        override_config_dict = None

    with open(config_path, 'r') as config_file:
        raw_config_dict = yaml.safe_load(config_file)
        if override_config_dict:
            raw_config_dict = _merge_configs(
                raw_config_dict,
                override_config_dict,
            )

        err_msg, config_dict = validate_config(raw_config_dict)

        if err_msg is not None:
            raise InvalidConfigError(str(err_msg))

        return config_dict


def init_configs():

    # todo fix this hack
    config_path, override_config_path = 'config/dev/app.yaml', None
    # config_path = os.environ.get('CONFIG')
    # override_config_path = os.environ.get('OVERRIDE_CONFIG')
    # if not config_path:
    #     raise ConfigNotSpecified(
    #         'Config should be specified with env var CONFIG'
    #     )

    raw_config = read_config(config_path, override_config_path)
    Config.init_from_dict(raw_config)


def get_config() -> Config:
    if not config:
        init_configs()

    return config
