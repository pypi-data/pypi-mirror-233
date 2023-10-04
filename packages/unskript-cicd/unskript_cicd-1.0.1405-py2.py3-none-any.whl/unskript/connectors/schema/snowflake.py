from pydantic import BaseModel, Field, SecretStr

class SnowflakeSchema(BaseModel):
    user: str = Field(
        title='User',
        description='Username'
    )
    password: SecretStr = Field(
        '',
        title='Password',
        description='Password to authenticate with Snowflake.'
    )
    account: str = Field(
        title='Account name',
        description='Name of the account to connect to.'
    )
