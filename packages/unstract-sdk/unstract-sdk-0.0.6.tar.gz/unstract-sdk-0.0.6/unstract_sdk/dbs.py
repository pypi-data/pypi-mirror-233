import os
from typing import Any

import requests
from unstract_sdk.constants import DbConnectorKeys, PlatformServiceKeys
from unstract_sdk.tools import UnstractToolUtils

from pandora_core.connectors.databases import connectors
from pandora_core.connectors.databases.pandora_db import PandoraDB


class UnstractToolDB:
    def __init__(
        self,
        utils: UnstractToolUtils,
        organization_id: str,
        platform_host: str,
        platform_port: str,
    ) -> None:
        self.utils = utils
        if platform_host[-1] == "/":
            self.base_url = f"{platform_host[:-1]}:{platform_port}"
        self.base_url = f"{platform_host}:{platform_port}/db"
        self.bearer_token = os.environ.get(PlatformServiceKeys.PLATFORM_API_KEY)
        self.organization_id = organization_id
        self.db_connectors = connectors

    def get_engine(self, project_id: str, connector_id: str) -> Any:
        """
        1. Get the connection settings (including auth for db)
        from platform service using the project_id and connector_name
        2. Create PandoraDB based object using the settings
            2.1 Find the type of the database (e.g. Snowflake, MySQL, etc.)
            2.2 Create the object using the type
            (derived class of PandoraDB) (Mysql/Postgresql/Bigquery/Snowflake/...)
        3. Send Object.get_engine() to the caller
        """
        if connector_id in self.db_connectors:
            url = f"{self.base_url}/engine"
            query_params = {
                DbConnectorKeys.PROJECT_ID: project_id,
                DbConnectorKeys.CONNECTOR_ID: connector_id,
            }
            headers = {
                "Authorization": f"Bearer {self.bearer_token}",
                DbConnectorKeys.ORGANIZATION_ID_HEADER: self.organization_id,
            }
            response = requests.get(url, headers=headers, params=query_params)
            if response.status_code == 200:
                self.utils.stream_log(
                    "Successfully retrieved connector settings "
                    f"for connector: {connector_id}"
                )
                settings = response.json()
                connector = self.db_connectors[connector_id]["metadata"]["connector"]
                connector_calss: PandoraDB = connector(settings)
                return connector_calss.get_engine()
            elif response.status_code == 404:
                self.utils.stream_log(
                    (f"settings not found for " f"connector: {connector_id}"),
                    level="WARN",
                )
                return None
            else:
                self.utils.stream_log(
                    (
                        f"Error while retrieving connector "
                        "settings for connector: "
                        f"{connector_id} / {response.reason}"
                    ),
                    level="ERROR",
                )
                return None
        else:
            self.utils.stream_log(
                f"engine not found for connector: {connector_id}", level="ERROR"
            )
            return None
