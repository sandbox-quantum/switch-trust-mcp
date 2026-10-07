from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.api_client_storage_put_request import ApiClientStoragePutRequest
from ...models.common_request_error import CommonRequestError
from typing import cast


def _get_kwargs(
    tenant_id: str,
    client_id: str,
    namespace: str,
    key: str,
    *,
    body: ApiClientStoragePutRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/client-storage/tenants/{tenant_id}/{client_id}/{namespace}/{key}".format(
            tenant_id=quote(str(tenant_id), safe=""),
            client_id=quote(str(client_id), safe=""),
            namespace=quote(str(namespace), safe=""),
            key=quote(str(key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | CommonRequestError | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = CommonRequestError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CommonRequestError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = CommonRequestError.from_dict(response.json())

        return response_403

    if response.status_code == 500:
        response_500 = CommonRequestError.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | CommonRequestError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    client_id: str,
    namespace: str,
    key: str,
    *,
    client: AuthenticatedClient,
    body: ApiClientStoragePutRequest,
) -> Response[Any | CommonRequestError]:
    """
    Args:
        tenant_id (str):
        client_id (str):
        namespace (str):
        key (str):
        body (ApiClientStoragePutRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CommonRequestError]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        client_id=client_id,
        namespace=namespace,
        key=key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    client_id: str,
    namespace: str,
    key: str,
    *,
    client: AuthenticatedClient,
    body: ApiClientStoragePutRequest,
) -> Any | CommonRequestError | None:
    """
    Args:
        tenant_id (str):
        client_id (str):
        namespace (str):
        key (str):
        body (ApiClientStoragePutRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CommonRequestError
    """

    return sync_detailed(
        tenant_id=tenant_id,
        client_id=client_id,
        namespace=namespace,
        key=key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    client_id: str,
    namespace: str,
    key: str,
    *,
    client: AuthenticatedClient,
    body: ApiClientStoragePutRequest,
) -> Response[Any | CommonRequestError]:
    """
    Args:
        tenant_id (str):
        client_id (str):
        namespace (str):
        key (str):
        body (ApiClientStoragePutRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CommonRequestError]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        client_id=client_id,
        namespace=namespace,
        key=key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    client_id: str,
    namespace: str,
    key: str,
    *,
    client: AuthenticatedClient,
    body: ApiClientStoragePutRequest,
) -> Any | CommonRequestError | None:
    """
    Args:
        tenant_id (str):
        client_id (str):
        namespace (str):
        key (str):
        body (ApiClientStoragePutRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CommonRequestError
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            client_id=client_id,
            namespace=namespace,
            key=key,
            client=client,
            body=body,
        )
    ).parsed
