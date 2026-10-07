from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_request_error import CommonRequestError
from ...models.engine_output_aispm_llm_session_detail import (
    EngineOutputAispmLlmSessionDetail,
)
from typing import cast


def _get_kwargs(
    tenant_id: str,
    workspace_id: str,
    session_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/aispm-llm-sessions/tenants/{tenant_id}/workspaces/{workspace_id}/{session_id}".format(
            tenant_id=quote(str(tenant_id), safe=""),
            workspace_id=quote(str(workspace_id), safe=""),
            session_id=quote(str(session_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonRequestError | EngineOutputAispmLlmSessionDetail | None:
    if response.status_code == 200:
        response_200 = EngineOutputAispmLlmSessionDetail.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = CommonRequestError.from_dict(response.json())

        return response_400

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
) -> Response[CommonRequestError | EngineOutputAispmLlmSessionDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    workspace_id: str,
    session_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[CommonRequestError | EngineOutputAispmLlmSessionDetail]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | EngineOutputAispmLlmSessionDetail]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        session_id=session_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    workspace_id: str,
    session_id: str,
    *,
    client: AuthenticatedClient,
) -> CommonRequestError | EngineOutputAispmLlmSessionDetail | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | EngineOutputAispmLlmSessionDetail
    """

    return sync_detailed(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        session_id=session_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    workspace_id: str,
    session_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[CommonRequestError | EngineOutputAispmLlmSessionDetail]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | EngineOutputAispmLlmSessionDetail]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        session_id=session_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    workspace_id: str,
    session_id: str,
    *,
    client: AuthenticatedClient,
) -> CommonRequestError | EngineOutputAispmLlmSessionDetail | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | EngineOutputAispmLlmSessionDetail
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            session_id=session_id,
            client=client,
        )
    ).parsed
