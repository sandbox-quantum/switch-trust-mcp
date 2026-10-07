from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_request_error import CommonRequestError
from ...models.engine_output_rule_info import EngineOutputRuleInfo
from typing import cast


def _get_kwargs(
    tenant_id: str,
    workspace_id: str,
    rule_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/rules/tenants/{tenant_id}/workspaces/{workspace_id}/{rule_id}".format(
            tenant_id=quote(str(tenant_id), safe=""),
            workspace_id=quote(str(workspace_id), safe=""),
            rule_id=quote(str(rule_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonRequestError | EngineOutputRuleInfo | None:
    if response.status_code == 200:
        response_200 = EngineOutputRuleInfo.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = CommonRequestError.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = CommonRequestError.from_dict(response.json())

        return response_404

    if response.status_code == 500:
        response_500 = CommonRequestError.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CommonRequestError | EngineOutputRuleInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    workspace_id: str,
    rule_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[CommonRequestError | EngineOutputRuleInfo]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        rule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | EngineOutputRuleInfo]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        rule_id=rule_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    workspace_id: str,
    rule_id: str,
    *,
    client: AuthenticatedClient,
) -> CommonRequestError | EngineOutputRuleInfo | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        rule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | EngineOutputRuleInfo
    """

    return sync_detailed(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        rule_id=rule_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    workspace_id: str,
    rule_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[CommonRequestError | EngineOutputRuleInfo]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        rule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | EngineOutputRuleInfo]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        rule_id=rule_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    workspace_id: str,
    rule_id: str,
    *,
    client: AuthenticatedClient,
) -> CommonRequestError | EngineOutputRuleInfo | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        rule_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | EngineOutputRuleInfo
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            rule_id=rule_id,
            client=client,
        )
    ).parsed
