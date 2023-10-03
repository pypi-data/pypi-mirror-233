"""
Main interface for bedrock service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_bedrock import (
        BedrockClient,
        Client,
        ListCustomModelsPaginator,
        ListModelCustomizationJobsPaginator,
        ListProvisionedModelThroughputsPaginator,
    )

    session = Session()
    client: BedrockClient = session.client("bedrock")

    list_custom_models_paginator: ListCustomModelsPaginator = client.get_paginator("list_custom_models")
    list_model_customization_jobs_paginator: ListModelCustomizationJobsPaginator = client.get_paginator("list_model_customization_jobs")
    list_provisioned_model_throughputs_paginator: ListProvisionedModelThroughputsPaginator = client.get_paginator("list_provisioned_model_throughputs")
    ```
"""
from .client import BedrockClient
from .paginator import (
    ListCustomModelsPaginator,
    ListModelCustomizationJobsPaginator,
    ListProvisionedModelThroughputsPaginator,
)

Client = BedrockClient

__all__ = (
    "BedrockClient",
    "Client",
    "ListCustomModelsPaginator",
    "ListModelCustomizationJobsPaginator",
    "ListProvisionedModelThroughputsPaginator",
)
