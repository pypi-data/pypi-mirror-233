##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field

'''
credentials is the json.dumps of the GCP credential json file.
'''
class GCPSchema(BaseModel):
    credentials: str = Field(
        title='Google Cloud Credentials JSON',
        description='Contents of the Google Cloud Credentials JSON file.'
    )