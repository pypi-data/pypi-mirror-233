##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field
from typing import Optional

class PrometheusSchema(BaseModel):
    url: str = Field(
        title='URL',
        description='url for the prometheus host.'
    )
    headers: Optional[dict] = Field(
        title='Headers',
        description=' A dictionary of http headers to be used to communicate with the host. Example: {“Authorization”: “bearer my_oauth_token_to_the_host”}'
    )
    disable_ssl: bool = Field(
        False,
        title='Disable ssl',
        description='If set to True, will disable ssl certificate verification for the http requests made to the prometheus host.'
    )
