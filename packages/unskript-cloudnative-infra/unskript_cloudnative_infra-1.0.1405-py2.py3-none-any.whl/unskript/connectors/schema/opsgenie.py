##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr

class OpsgenieSchema(BaseModel):
    api_token: SecretStr = Field(
        title='Api Token',
        description='Api token to authenticate Opsgenie: GenieKey'
    )

