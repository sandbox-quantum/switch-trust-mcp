from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.gateway_api_key_result import GatewayAPIKeyResult
from ...models.gateway_create_api_key_request import GatewayCreateAPIKeyRequest
from ...models.gateway_error_response import GatewayErrorResponse
from typing import cast


def _get_kwargs(
    *,
    body: GatewayCreateAPIKeyRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api-keys",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GatewayAPIKeyResult | GatewayErrorResponse | None:
    if response.status_code == 201:
        response_201 = GatewayAPIKeyResult.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = GatewayErrorResponse.from_dict(response.json())

        return response_400

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
) -> Response[GatewayAPIKeyResult | GatewayErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: GatewayCreateAPIKeyRequest,
) -> Response[GatewayAPIKeyResult | GatewayErrorResponse]:
    """
    Args:
        body (GatewayCreateAPIKeyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GatewayAPIKeyResult | GatewayErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: GatewayCreateAPIKeyRequest,
) -> GatewayAPIKeyResult | GatewayErrorResponse | None:
    """
    Args:
        body (GatewayCreateAPIKeyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GatewayAPIKeyResult | GatewayErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: GatewayCreateAPIKeyRequest,
) -> Response[GatewayAPIKeyResult | GatewayErrorResponse]:
    """
    Args:
        body (GatewayCreateAPIKeyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GatewayAPIKeyResult | GatewayErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: GatewayCreateAPIKeyRequest,
) -> GatewayAPIKeyResult | GatewayErrorResponse | None:
    """
    Args:
        body (GatewayCreateAPIKeyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GatewayAPIKeyResult | GatewayErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
