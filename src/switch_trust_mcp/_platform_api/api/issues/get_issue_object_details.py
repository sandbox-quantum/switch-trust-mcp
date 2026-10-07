from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_request_error import CommonRequestError
from ...models.get_issue_object_details_response_200 import (
    GetIssueObjectDetailsResponse200,
)
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    tenant_id: str,
    workspace_id: str,
    id: str,
    object_id: str,
    *,
    page_size: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["page_size"] = page_size

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/issues/tenants/{tenant_id}/workspaces/{workspace_id}/{id}/objects/{object_id}/details".format(
            tenant_id=quote(str(tenant_id), safe=""),
            workspace_id=quote(str(workspace_id), safe=""),
            id=quote(str(id), safe=""),
            object_id=quote(str(object_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonRequestError | GetIssueObjectDetailsResponse200 | None:
    if response.status_code == 200:
        response_200 = GetIssueObjectDetailsResponse200.from_dict(response.json())

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

    if response.status_code == 500:
        response_500 = CommonRequestError.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CommonRequestError | GetIssueObjectDetailsResponse200]:
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
    *,
    client: AuthenticatedClient,
    page_size: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[CommonRequestError | GetIssueObjectDetailsResponse200]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        id (str):
        object_id (str):
        page_size (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | GetIssueObjectDetailsResponse200]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        id=id,
        object_id=object_id,
        page_size=page_size,
        cursor=cursor,
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
    *,
    client: AuthenticatedClient,
    page_size: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> CommonRequestError | GetIssueObjectDetailsResponse200 | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        id (str):
        object_id (str):
        page_size (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | GetIssueObjectDetailsResponse200
    """

    return sync_detailed(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        id=id,
        object_id=object_id,
        client=client,
        page_size=page_size,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    workspace_id: str,
    id: str,
    object_id: str,
    *,
    client: AuthenticatedClient,
    page_size: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[CommonRequestError | GetIssueObjectDetailsResponse200]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        id (str):
        object_id (str):
        page_size (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | GetIssueObjectDetailsResponse200]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        id=id,
        object_id=object_id,
        page_size=page_size,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    workspace_id: str,
    id: str,
    object_id: str,
    *,
    client: AuthenticatedClient,
    page_size: int | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> CommonRequestError | GetIssueObjectDetailsResponse200 | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        id (str):
        object_id (str):
        page_size (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | GetIssueObjectDetailsResponse200
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            id=id,
            object_id=object_id,
            client=client,
            page_size=page_size,
            cursor=cursor,
        )
    ).parsed
