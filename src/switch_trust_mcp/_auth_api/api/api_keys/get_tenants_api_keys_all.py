from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.gateway_error_response import GatewayErrorResponse
from ...models.gateway_paginated_response_gateway_api_key_info import (
    GatewayPaginatedResponseGatewayAPIKeyInfo,
)
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    *,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/tenants/api-keys/all",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GatewayErrorResponse | GatewayPaginatedResponseGatewayAPIKeyInfo | None:
    if response.status_code == 200:
        response_200 = GatewayPaginatedResponseGatewayAPIKeyInfo.from_dict(
            response.json()
        )

        return response_200

    if response.status_code == 401:
        response_401 = GatewayErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GatewayErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 500:
        response_500 = GatewayErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GatewayErrorResponse | GatewayPaginatedResponseGatewayAPIKeyInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
) -> Response[GatewayErrorResponse | GatewayPaginatedResponseGatewayAPIKeyInfo]:
    """
    Args:
        limit (int | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GatewayErrorResponse | GatewayPaginatedResponseGatewayAPIKeyInfo]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
) -> GatewayErrorResponse | GatewayPaginatedResponseGatewayAPIKeyInfo | None:
    """
    Args:
        limit (int | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GatewayErrorResponse | GatewayPaginatedResponseGatewayAPIKeyInfo
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
) -> Response[GatewayErrorResponse | GatewayPaginatedResponseGatewayAPIKeyInfo]:
    """
    Args:
        limit (int | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GatewayErrorResponse | GatewayPaginatedResponseGatewayAPIKeyInfo]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
) -> GatewayErrorResponse | GatewayPaginatedResponseGatewayAPIKeyInfo | None:
    """
    Args:
        limit (int | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GatewayErrorResponse | GatewayPaginatedResponseGatewayAPIKeyInfo
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
        )
    ).parsed
