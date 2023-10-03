"""
Type annotations for bedrock-runtime service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_runtime/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_bedrock_runtime.client import BedrockRuntimeClient

    session = Session()
    client: BedrockRuntimeClient = session.client("bedrock-runtime")
    ```
"""
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .type_defs import (
    BlobTypeDef,
    InvokeModelResponseTypeDef,
    InvokeModelWithResponseStreamResponseTypeDef,
)

__all__ = ("BedrockRuntimeClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ModelErrorException: Type[BotocoreClientError]
    ModelNotReadyException: Type[BotocoreClientError]
    ModelStreamErrorException: Type[BotocoreClientError]
    ModelTimeoutException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class BedrockRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html#BedrockRuntime.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BedrockRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html#BedrockRuntime.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html#BedrockRuntime.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_runtime/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html#BedrockRuntime.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_runtime/client/#close)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html#BedrockRuntime.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_runtime/client/#generate_presigned_url)
        """

    def invoke_model(
        self, *, body: BlobTypeDef, modelId: str, accept: str = ..., contentType: str = ...
    ) -> InvokeModelResponseTypeDef:
        """
        Invokes the specified Bedrock model to run inference using the input provided
        in the request
        body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html#BedrockRuntime.Client.invoke_model)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_runtime/client/#invoke_model)
        """

    def invoke_model_with_response_stream(
        self, *, body: BlobTypeDef, modelId: str, accept: str = ..., contentType: str = ...
    ) -> InvokeModelWithResponseStreamResponseTypeDef:
        """
        Invoke the specified Bedrock model to run inference using the input provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html#BedrockRuntime.Client.invoke_model_with_response_stream)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_runtime/client/#invoke_model_with_response_stream)
        """
