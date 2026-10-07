from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.gateway_error_response import GatewayErrorResponse
from ...models.gateway_update_member_request import GatewayUpdateMemberRequest
from ...models.gateway_update_member_role_result import GatewayUpdateMemberRoleResult
from typing import cast


def _get_kwargs(
    id: str,
    *,
    body: GatewayUpdateMemberRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/tenants/members/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GatewayErrorResponse | GatewayUpdateMemberRoleResult | None:
    if response.status_code == 200:
        response_200 = GatewayUpdateMemberRoleResult.from_dict(response.json())

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

    if response.status_code == 404:
        response_404 = GatewayErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = GatewayErrorResponse.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GatewayErrorResponse | GatewayUpdateMemberRoleResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: GatewayUpdateMemberRequest,
) -> Response[GatewayErrorResponse | GatewayUpdateMemberRoleResult]:
    """
    Args:
        id (str):
        body (GatewayUpdateMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GatewayErrorResponse | GatewayUpdateMemberRoleResult]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: GatewayUpdateMemberRequest,
) -> GatewayErrorResponse | GatewayUpdateMemberRoleResult | None:
    """
    Args:
        id (str):
        body (GatewayUpdateMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GatewayErrorResponse | GatewayUpdateMemberRoleResult
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: GatewayUpdateMemberRequest,
) -> Response[GatewayErrorResponse | GatewayUpdateMemberRoleResult]:
    """
    Args:
        id (str):
        body (GatewayUpdateMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GatewayErrorResponse | GatewayUpdateMemberRoleResult]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: GatewayUpdateMemberRequest,
) -> GatewayErrorResponse | GatewayUpdateMemberRoleResult | None:
    """
    Args:
        id (str):
        body (GatewayUpdateMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GatewayErrorResponse | GatewayUpdateMemberRoleResult
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
