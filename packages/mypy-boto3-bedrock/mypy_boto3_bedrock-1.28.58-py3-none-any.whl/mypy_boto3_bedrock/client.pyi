"""
Type annotations for bedrock service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_bedrock.client import BedrockClient

    session = Session()
    client: BedrockClient = session.client("bedrock")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    CommitmentDurationType,
    FineTuningJobStatusType,
    InferenceTypeType,
    ModelModalityType,
    ProvisionedModelStatusType,
    SortOrderType,
)
from .paginator import (
    ListCustomModelsPaginator,
    ListModelCustomizationJobsPaginator,
    ListProvisionedModelThroughputsPaginator,
)
from .type_defs import (
    CreateModelCustomizationJobResponseTypeDef,
    CreateProvisionedModelThroughputResponseTypeDef,
    GetCustomModelResponseTypeDef,
    GetFoundationModelResponseTypeDef,
    GetModelCustomizationJobResponseTypeDef,
    GetModelInvocationLoggingConfigurationResponseTypeDef,
    GetProvisionedModelThroughputResponseTypeDef,
    ListCustomModelsResponseTypeDef,
    ListFoundationModelsResponseTypeDef,
    ListModelCustomizationJobsResponseTypeDef,
    ListProvisionedModelThroughputsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    LoggingConfigTypeDef,
    OutputDataConfigTypeDef,
    TagTypeDef,
    TimestampTypeDef,
    TrainingDataConfigTypeDef,
    ValidationDataConfigTypeDef,
    VpcConfigTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("BedrockClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class BedrockClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BedrockClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#close)
        """

    def create_model_customization_job(
        self,
        *,
        jobName: str,
        customModelName: str,
        roleArn: str,
        baseModelIdentifier: str,
        trainingDataConfig: TrainingDataConfigTypeDef,
        outputDataConfig: OutputDataConfigTypeDef,
        hyperParameters: Mapping[str, str],
        clientRequestToken: str = ...,
        customModelKmsKeyId: str = ...,
        jobTags: Sequence[TagTypeDef] = ...,
        customModelTags: Sequence[TagTypeDef] = ...,
        validationDataConfig: ValidationDataConfigTypeDef = ...,
        vpcConfig: VpcConfigTypeDef = ...
    ) -> CreateModelCustomizationJobResponseTypeDef:
        """
        Creates a fine-tuning job to customize a base model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.create_model_customization_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#create_model_customization_job)
        """

    def create_provisioned_model_throughput(
        self,
        *,
        modelUnits: int,
        provisionedModelName: str,
        modelId: str,
        clientRequestToken: str = ...,
        commitmentDuration: CommitmentDurationType = ...,
        tags: Sequence[TagTypeDef] = ...
    ) -> CreateProvisionedModelThroughputResponseTypeDef:
        """
        Creates a provisioned throughput with dedicated capacity for a foundation model
        or a fine-tuned
        model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.create_provisioned_model_throughput)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#create_provisioned_model_throughput)
        """

    def delete_custom_model(self, *, modelIdentifier: str) -> Dict[str, Any]:
        """
        Deletes a custom model that you created earlier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.delete_custom_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#delete_custom_model)
        """

    def delete_model_invocation_logging_configuration(self) -> Dict[str, Any]:
        """
        Delete the invocation logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.delete_model_invocation_logging_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#delete_model_invocation_logging_configuration)
        """

    def delete_provisioned_model_throughput(self, *, provisionedModelId: str) -> Dict[str, Any]:
        """
        Deletes a provisioned throughput.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.delete_provisioned_model_throughput)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#delete_provisioned_model_throughput)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#generate_presigned_url)
        """

    def get_custom_model(self, *, modelIdentifier: str) -> GetCustomModelResponseTypeDef:
        """
        Get the properties associated with a Bedrock custom model that you have
        created.For more information, see [Custom
        models](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html)
        in the Bedrock User
        Guide.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.get_custom_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#get_custom_model)
        """

    def get_foundation_model(self, *, modelIdentifier: str) -> GetFoundationModelResponseTypeDef:
        """
        Get details about a Bedrock foundation model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.get_foundation_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#get_foundation_model)
        """

    def get_model_customization_job(
        self, *, jobIdentifier: str
    ) -> GetModelCustomizationJobResponseTypeDef:
        """
        Retrieves the properties associated with a model-customization job, including
        the status of the
        job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.get_model_customization_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#get_model_customization_job)
        """

    def get_model_invocation_logging_configuration(
        self,
    ) -> GetModelInvocationLoggingConfigurationResponseTypeDef:
        """
        Get the current configuration values for model invocation logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.get_model_invocation_logging_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#get_model_invocation_logging_configuration)
        """

    def get_provisioned_model_throughput(
        self, *, provisionedModelId: str
    ) -> GetProvisionedModelThroughputResponseTypeDef:
        """
        Get details for a provisioned throughput.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.get_provisioned_model_throughput)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#get_provisioned_model_throughput)
        """

    def list_custom_models(
        self,
        *,
        creationTimeBefore: TimestampTypeDef = ...,
        creationTimeAfter: TimestampTypeDef = ...,
        nameContains: str = ...,
        baseModelArnEquals: str = ...,
        foundationModelArnEquals: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        sortBy: Literal["CreationTime"] = ...,
        sortOrder: SortOrderType = ...
    ) -> ListCustomModelsResponseTypeDef:
        """
        Returns a list of the custom models that you have created with the
        `CreateModelCustomizationJob`
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.list_custom_models)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#list_custom_models)
        """

    def list_foundation_models(
        self,
        *,
        byProvider: str = ...,
        byCustomizationType: Literal["FINE_TUNING"] = ...,
        byOutputModality: ModelModalityType = ...,
        byInferenceType: InferenceTypeType = ...
    ) -> ListFoundationModelsResponseTypeDef:
        """
        List of Bedrock foundation models that you can use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.list_foundation_models)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#list_foundation_models)
        """

    def list_model_customization_jobs(
        self,
        *,
        creationTimeAfter: TimestampTypeDef = ...,
        creationTimeBefore: TimestampTypeDef = ...,
        statusEquals: FineTuningJobStatusType = ...,
        nameContains: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        sortBy: Literal["CreationTime"] = ...,
        sortOrder: SortOrderType = ...
    ) -> ListModelCustomizationJobsResponseTypeDef:
        """
        Returns a list of model customization jobs that you have submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.list_model_customization_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#list_model_customization_jobs)
        """

    def list_provisioned_model_throughputs(
        self,
        *,
        creationTimeAfter: TimestampTypeDef = ...,
        creationTimeBefore: TimestampTypeDef = ...,
        statusEquals: ProvisionedModelStatusType = ...,
        modelArnEquals: str = ...,
        nameContains: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        sortBy: Literal["CreationTime"] = ...,
        sortOrder: SortOrderType = ...
    ) -> ListProvisionedModelThroughputsResponseTypeDef:
        """
        List the provisioned capacities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.list_provisioned_model_throughputs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#list_provisioned_model_throughputs)
        """

    def list_tags_for_resource(self, *, resourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#list_tags_for_resource)
        """

    def put_model_invocation_logging_configuration(
        self, *, loggingConfig: LoggingConfigTypeDef
    ) -> Dict[str, Any]:
        """
        Set the configuration values for model invocation logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.put_model_invocation_logging_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#put_model_invocation_logging_configuration)
        """

    def stop_model_customization_job(self, *, jobIdentifier: str) -> Dict[str, Any]:
        """
        Stops an active model customization job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.stop_model_customization_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#stop_model_customization_job)
        """

    def tag_resource(self, *, resourceARN: str, tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Associate tags with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#tag_resource)
        """

    def untag_resource(self, *, resourceARN: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Remove one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#untag_resource)
        """

    def update_provisioned_model_throughput(
        self,
        *,
        provisionedModelId: str,
        desiredProvisionedModelName: str = ...,
        desiredModelId: str = ...
    ) -> Dict[str, Any]:
        """
        Update a provisioned throughput.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.update_provisioned_model_throughput)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#update_provisioned_model_throughput)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_models"]
    ) -> ListCustomModelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_customization_jobs"]
    ) -> ListModelCustomizationJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provisioned_model_throughputs"]
    ) -> ListProvisionedModelThroughputsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html#Bedrock.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/client/#get_paginator)
        """
