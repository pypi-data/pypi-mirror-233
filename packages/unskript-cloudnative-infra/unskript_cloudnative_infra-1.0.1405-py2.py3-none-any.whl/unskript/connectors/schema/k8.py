##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field


'''
kubeconfig is the contents of the kubeconfig file.
'''
class K8Schema(BaseModel):
    kubeconfig: str = Field(
        title='Kubeconfig',
        description='Contents of the kubeconfig file.'
    )