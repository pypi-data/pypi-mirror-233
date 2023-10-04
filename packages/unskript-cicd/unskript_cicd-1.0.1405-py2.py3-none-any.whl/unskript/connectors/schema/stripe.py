##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr


class StripeSchema(BaseModel):
    api_key: SecretStr = Field(
        title = 'API Key',
        description = 'API secret or publish key to authenticate to stripe.'
    )
