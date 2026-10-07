from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.gateway_error_response import GatewayErrorResponse
from ...models.gateway_payment_method_info import GatewayPaymentMethodInfo
from typing import cast


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/billing/payment-method",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GatewayErrorResponse | GatewayPaymentMethodInfo | None:
    if response.status_code == 200:
        response_200 = GatewayPaymentMethodInfo.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = GatewayErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = GatewayErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = GatewayErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 502:
        response_502 = GatewayErrorResponse.from_dict(response.json())

        return response_502

    if response.status_code == 503:
        response_503 = GatewayErrorResponse.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GatewayErrorResponse | GatewayPaymentMethodInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GatewayErrorResponse | GatewayPaymentMethodInfo]:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GatewayErrorResponse | GatewayPaymentMethodInfo]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> GatewayErrorResponse | GatewayPaymentMethodInfo | None:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GatewayErrorResponse | GatewayPaymentMethodInfo
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[GatewayErrorResponse | GatewayPaymentMethodInfo]:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GatewayErrorResponse | GatewayPaymentMethodInfo]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> GatewayErrorResponse | GatewayPaymentMethodInfo | None:
    """
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GatewayErrorResponse | GatewayPaymentMethodInfo
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
