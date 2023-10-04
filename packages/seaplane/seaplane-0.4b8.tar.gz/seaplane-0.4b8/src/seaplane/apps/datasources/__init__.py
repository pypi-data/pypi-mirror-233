import json
import time
from typing import Dict, Optional, cast

import seaplane_framework.api
from seaplane_framework.api.apis.tags import key_value_api
import seaplane_framework.api.schemas

from ...api.api_request import provision_token
from ...api.sql_api import GlobalSQL
from ...configuration import Configuration, config
from ...logging import log
from ...model.sql import CreatedDatabase
from ...util import unwrap
from .sql_executor import SqlExecutor

_DEFAULT_KV_STORE_NAME = "_SEAPLANE_INTERNAL"
_DEFAULT_KV_STORE_CONFIG = {
    "max_value_size": 16777216,
    "history": 16,
    "replicas": 3,
    "allow_locations": ["all"],
}


def _make_default_kvstore(token: str, cfg: Configuration = config) -> None:
    platform_cfg = cfg.get_platform_configuration()
    platform_cfg.access_token = token
    with seaplane_framework.api.ApiClient(platform_cfg) as api:
        kv = key_value_api.KeyValueApi(api)
        resp = kv.list_stores()
        if _DEFAULT_KV_STORE_NAME in resp.body:
            return
        kv.create_store(
            path_params={"kv_store": _DEFAULT_KV_STORE_NAME},
            body=_DEFAULT_KV_STORE_CONFIG,
        )


requests_table = """
CREATE TABLE requests (
     id VARCHAR PRIMARY KEY,
     batch_count INTEGER
);
"""

results_table = """
CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR,
    original_order INTEGER,
    output JSONB
);
"""


def _create_schema(database: CreatedDatabase) -> None:
    attempts = 0
    exit = False
    log.debug("Creating db schemas...")

    while attempts < 3 and not exit:
        try:
            sql = SqlExecutor.from_seaplane_database(database)

            sql.execute(requests_table)
            sql.execute(results_table)
            exit = True
        except Exception as e:
            log.error(f"Create schema error: {e}")
            attempts = attempts + 1
            log.error(f"attempt: {attempts}")

    if attempts == 3:
        log.debug("Error creating the default DB tables")


def _get_default_db_info() -> Optional[Dict[str, str]]:
    def _inner(token: str) -> Optional[Dict[str, str]]:
        _make_default_kvstore(token=token)
        platform_cfg = config.get_platform_configuration()
        platform_cfg.access_token = token
        with seaplane_framework.api.ApiClient(platform_cfg) as api:
            kv = key_value_api.KeyValueApi(api)
            try:
                raw_ret = kv.get_key(
                    path_params={
                        "kv_store": _DEFAULT_KV_STORE_NAME,
                        "key": "default_db",
                    },
                    stream=True,
                    accept_content_types=("application/octet-stream",),
                    timeout=300,
                    skip_deserialization=True,
                )
                data = raw_ret.response.read()
                return cast(Dict[str, str], json.loads(data.decode()))
            except seaplane_framework.api.ApiException as e:
                if e.status == 404:
                    return None
                else:
                    raise e

    req = provision_token(config._token_api)
    return cast(Dict[str, str], unwrap(req(_inner)))


def _put_database(created_database: CreatedDatabase) -> None:
    def _inner(token: str) -> None:
        _make_default_kvstore(token=token)
        platform_cfg = config.get_platform_configuration()
        platform_cfg.access_token = token
        with seaplane_framework.api.ApiClient(platform_cfg) as api:
            kv = key_value_api.KeyValueApi(api)
            kv.put_key(
                path_params={"kv_store": _DEFAULT_KV_STORE_NAME, "key": "default_db"},
                body=json.dumps(created_database._asdict()).encode(),
            )

    req = provision_token(config._token_api)

    unwrap(req(_inner))


def tenant_database() -> CreatedDatabase:
    default_db = _get_default_db_info()

    if not default_db:
        log.debug("Default DB doesn't exist, creating DB...")
        sql = GlobalSQL(config)
        new_database = sql.create_database()

        databases = sql.list_databases()

        while new_database.name not in databases:
            databases = sql.list_databases()
            time.sleep(1)

        _create_schema(new_database)
        _put_database(new_database)

        return new_database
    else:
        return CreatedDatabase(**default_db)


__all__ = ["SqlExecutor"]
