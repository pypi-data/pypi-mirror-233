##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field, SecretStr
from typing import Optional

class ChatGPTSchema(BaseModel):
    organization: Optional[str] =Field(
        '',
        title='Organization ID',
        description='Identifier for the organization which is sometimes used in API requests. Eg: org-s8OPLNKVjsDAjjdbfTuhqAc'
    )
    api_token: SecretStr = Field(
        title='API Token',
        description='API Token value to authenticate requests.'
    )