from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_request_error import CommonRequestError
from ...models.get_issue_object_detail_response_200 import (
    GetIssueObjectDetailResponse200,
)
from typing import cast


def _get_kwargs(
    tenant_id: str,
    workspace_id: str,
    id: str,
    object_id: str,
    detail_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/issues/tenants/{tenant_id}/workspaces/{workspace_id}/{id}/objects/{object_id}/details/{detail_id}".format(
            tenant_id=quote(str(tenant_id), safe=""),
            workspace_id=quote(str(workspace_id), safe=""),
            id=quote(str(id), safe=""),
            object_id=quote(str(object_id), safe=""),
            detail_id=quote(str(detail_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonRequestError | GetIssueObjectDetailResponse200 | None:
    if response.status_code == 200:
        response_200 = GetIssueObjectDetailResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = CommonRequestError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CommonRequestError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = CommonRequestError.from_dict(response.json())

        return response_403

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
) -> Response[CommonRequestError | GetIssueObjectDetailResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    workspace_id: str,
    id: str,
    object_id: str,
    detail_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[CommonRequestError | GetIssueObjectDetailResponse200]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        id (str):
        object_id (str):
        detail_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | GetIssueObjectDetailResponse200]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        id=id,
        object_id=object_id,
        detail_id=detail_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    workspace_id: str,
    id: str,
    object_id: str,
    detail_id: str,
    *,
    client: AuthenticatedClient,
) -> CommonRequestError | GetIssueObjectDetailResponse200 | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        id (str):
        object_id (str):
        detail_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | GetIssueObjectDetailResponse200
    """

    return sync_detailed(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        id=id,
        object_id=object_id,
        detail_id=detail_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    workspace_id: str,
    id: str,
    object_id: str,
    detail_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[CommonRequestError | GetIssueObjectDetailResponse200]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        id (str):
        object_id (str):
        detail_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | GetIssueObjectDetailResponse200]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        id=id,
        object_id=object_id,
        detail_id=detail_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    workspace_id: str,
    id: str,
    object_id: str,
    detail_id: str,
    *,
    client: AuthenticatedClient,
) -> CommonRequestError | GetIssueObjectDetailResponse200 | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        id (str):
        object_id (str):
        detail_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | GetIssueObjectDetailResponse200
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            id=id,
            object_id=object_id,
            detail_id=detail_id,
            client=client,
        )
    ).parsed
