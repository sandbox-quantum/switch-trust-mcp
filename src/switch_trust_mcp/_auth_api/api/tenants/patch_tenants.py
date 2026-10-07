from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.gateway_error_response import GatewayErrorResponse
from ...models.gateway_update_tenant_body import GatewayUpdateTenantBody
from ...models.gateway_update_tenant_response import GatewayUpdateTenantResponse
from typing import cast


def _get_kwargs(
    *,
    body: GatewayUpdateTenantBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/tenants",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GatewayErrorResponse | GatewayUpdateTenantResponse | None:
    if response.status_code == 200:
        response_200 = GatewayUpdateTenantResponse.from_dict(response.json())

        return response_200

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
) -> Response[GatewayErrorResponse | GatewayUpdateTenantResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: GatewayUpdateTenantBody,
) -> Response[GatewayErrorResponse | GatewayUpdateTenantResponse]:
    """
    Args:
        body (GatewayUpdateTenantBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GatewayErrorResponse | GatewayUpdateTenantResponse]
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
    body: GatewayUpdateTenantBody,
) -> GatewayErrorResponse | GatewayUpdateTenantResponse | None:
    """
    Args:
        body (GatewayUpdateTenantBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GatewayErrorResponse | GatewayUpdateTenantResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: GatewayUpdateTenantBody,
) -> Response[GatewayErrorResponse | GatewayUpdateTenantResponse]:
    """
    Args:
        body (GatewayUpdateTenantBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GatewayErrorResponse | GatewayUpdateTenantResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: GatewayUpdateTenantBody,
) -> GatewayErrorResponse | GatewayUpdateTenantResponse | None:
    """
    Args:
        body (GatewayUpdateTenantBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GatewayErrorResponse | GatewayUpdateTenantResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
