import os

from dotenv import load_dotenv
from oslo_config import cfg

from settings.constants import CONFIG_FILE

load_dotenv()


class ConfigService:
    service_group = cfg.OptGroup('service')

    service_opt = [
        cfg.StrOpt("host", default=os.getenv("HOST")),
        cfg.IntOpt("port", default=os.getenv("PORT"))
    ]
    conf = cfg.CONF
    conf(default_config_files=[CONFIG_FILE])
    conf.register_group(service_group)
    conf.register_opts(service_opt, group=service_group)
    HOST = cfg.CONF.service.host
    PORT = cfg.CONF.service.port




class ConfigDB:
    database_group = cfg.OptGroup('database')

    database_opt = [
        cfg.StrOpt("url", default=os.getenv("DB_URL")),
    ]
    conf = cfg.CONF
    conf(default_config_files=[CONFIG_FILE])
    conf.register_group(database_group)
    conf.register_opts(database_opt, group=database_group)
    DB_URL = cfg.CONF.database.url


class ConfigCelery:
    celery_group = cfg.OptGroup('celery')

    celery_opt = [
        cfg.StrOpt("broker", default=os.getenv("BROKER_URL")),
        cfg.StrOpt("backend", default=os.getenv("RESULT_BACKEND"))
    ]
    conf = cfg.CONF
    conf(default_config_files=[CONFIG_FILE])
    conf.register_group(celery_group)
    conf.register_opts(celery_opt, group=celery_group)
    BROKER = cfg.CONF.celery.broker
    BACKEND = cfg.CONF.celery.backend


class ConfigExchangeApi:
    api_group = cfg.OptGroup('api')

    api_opt = [
        cfg.StrOpt("api_key", default=os.getenv("API_KEY")),
        cfg.StrOpt("prices_url", default=os.getenv("PRICES_URL")),
        cfg.StrOpt("names_url", default=os.getenv("NAMES_URL")),
        cfg.StrOpt("db_sync_url", default=os.getenv("DB_SYNC_URL"))
    ]
    conf = cfg.CONF
    conf(default_config_files=[CONFIG_FILE])
    conf.register_group(api_group)
    conf.register_opts(api_opt, group=api_group)
    API_KEY = cfg.CONF.api.api_key
    PRICES_URL = cfg.CONF.api.prices_url
    NAMES_URL = cfg.CONF.api.names_url
    DB_URL = cfg.CONF.api.db_sync_url
