#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#

from pydantic import BaseModel, Field, SecretStr

class SalesforceSchema(BaseModel):
    Username: str = Field(
        title='Username',
        description='Username to authenticate to Salesforce.'
    )
    Password: SecretStr = Field(
        title='Password',
        description='Password to authenticate to Salesforce.'
    )
    Security_Token: str = Field(
        title='Security token',
        description='Token to authenticate to Salesforce.'
    )
