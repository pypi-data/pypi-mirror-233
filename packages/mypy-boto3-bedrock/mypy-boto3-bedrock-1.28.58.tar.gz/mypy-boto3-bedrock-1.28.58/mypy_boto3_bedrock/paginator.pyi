"""
Type annotations for bedrock service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_bedrock.client import BedrockClient
    from mypy_boto3_bedrock.paginator import (
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
import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import FineTuningJobStatusType, ProvisionedModelStatusType, SortOrderType
from .type_defs import (
    ListCustomModelsResponseTypeDef,
    ListModelCustomizationJobsResponseTypeDef,
    ListProvisionedModelThroughputsResponseTypeDef,
    PaginatorConfigTypeDef,
    TimestampTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ListCustomModelsPaginator",
    "ListModelCustomizationJobsPaginator",
    "ListProvisionedModelThroughputsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCustomModelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListCustomModels)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listcustommodelspaginator)
    """

    def paginate(
        self,
        *,
        creationTimeBefore: TimestampTypeDef = ...,
        creationTimeAfter: TimestampTypeDef = ...,
        nameContains: str = ...,
        baseModelArnEquals: str = ...,
        foundationModelArnEquals: str = ...,
        sortBy: Literal["CreationTime"] = ...,
        sortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCustomModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListCustomModels.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listcustommodelspaginator)
        """

class ListModelCustomizationJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListModelCustomizationJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listmodelcustomizationjobspaginator)
    """

    def paginate(
        self,
        *,
        creationTimeAfter: TimestampTypeDef = ...,
        creationTimeBefore: TimestampTypeDef = ...,
        statusEquals: FineTuningJobStatusType = ...,
        nameContains: str = ...,
        sortBy: Literal["CreationTime"] = ...,
        sortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListModelCustomizationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListModelCustomizationJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listmodelcustomizationjobspaginator)
        """

class ListProvisionedModelThroughputsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListProvisionedModelThroughputs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listprovisionedmodelthroughputspaginator)
    """

    def paginate(
        self,
        *,
        creationTimeAfter: TimestampTypeDef = ...,
        creationTimeBefore: TimestampTypeDef = ...,
        statusEquals: ProvisionedModelStatusType = ...,
        modelArnEquals: str = ...,
        nameContains: str = ...,
        sortBy: Literal["CreationTime"] = ...,
        sortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListProvisionedModelThroughputsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Paginator.ListProvisionedModelThroughputs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/paginators/#listprovisionedmodelthroughputspaginator)
        """
