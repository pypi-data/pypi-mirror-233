from typing import Any
import snowflake.connector
from pydantic import ValidationError

from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.schema.snowflake import SnowflakeSchema


class SnowflakeConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            snowflakeCredential = SnowflakeSchema(**data)
        except ValidationError as e:
            raise e

        try:
            snowflakeClient = snowflake.connector.connect(
                user=snowflakeCredential.user,
                password=snowflakeCredential.password.get_secret_value(),
                account=snowflakeCredential.account
            )
        except Exception as e:
            raise e

        return snowflakeClient
