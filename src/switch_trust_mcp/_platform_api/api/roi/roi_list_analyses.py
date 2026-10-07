from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_request_error import CommonRequestError
from ...models.roi_list_analyses_order import RoiListAnalysesOrder
from ...models.roi_list_analyses_result import RoiListAnalysesResult
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    tenant_id: str,
    workspace_id: str,
    *,
    agent_id: str | Unset = UNSET,
    analysis_type: str | Unset = UNSET,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
    order: RoiListAnalysesOrder | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["agent_id"] = agent_id

    params["analysis_type"] = analysis_type

    params["page"] = page

    params["page_size"] = page_size

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/roi/analyses/tenants/{tenant_id}/workspaces/{workspace_id}".format(
            tenant_id=quote(str(tenant_id), safe=""),
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonRequestError | RoiListAnalysesResult | None:
    if response.status_code == 200:
        response_200 = RoiListAnalysesResult.from_dict(response.json())

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
) -> Response[CommonRequestError | RoiListAnalysesResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    agent_id: str | Unset = UNSET,
    analysis_type: str | Unset = UNSET,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
    order: RoiListAnalysesOrder | Unset = UNSET,
) -> Response[CommonRequestError | RoiListAnalysesResult]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        agent_id (str | Unset):
        analysis_type (str | Unset):
        page (int | Unset):
        page_size (int | Unset):
        order (RoiListAnalysesOrder | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | RoiListAnalysesResult]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        agent_id=agent_id,
        analysis_type=analysis_type,
        page=page,
        page_size=page_size,
        order=order,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    agent_id: str | Unset = UNSET,
    analysis_type: str | Unset = UNSET,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
    order: RoiListAnalysesOrder | Unset = UNSET,
) -> CommonRequestError | RoiListAnalysesResult | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        agent_id (str | Unset):
        analysis_type (str | Unset):
        page (int | Unset):
        page_size (int | Unset):
        order (RoiListAnalysesOrder | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | RoiListAnalysesResult
    """

    return sync_detailed(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        client=client,
        agent_id=agent_id,
        analysis_type=analysis_type,
        page=page,
        page_size=page_size,
        order=order,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    agent_id: str | Unset = UNSET,
    analysis_type: str | Unset = UNSET,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
    order: RoiListAnalysesOrder | Unset = UNSET,
) -> Response[CommonRequestError | RoiListAnalysesResult]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        agent_id (str | Unset):
        analysis_type (str | Unset):
        page (int | Unset):
        page_size (int | Unset):
        order (RoiListAnalysesOrder | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | RoiListAnalysesResult]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        agent_id=agent_id,
        analysis_type=analysis_type,
        page=page,
        page_size=page_size,
        order=order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    agent_id: str | Unset = UNSET,
    analysis_type: str | Unset = UNSET,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
    order: RoiListAnalysesOrder | Unset = UNSET,
) -> CommonRequestError | RoiListAnalysesResult | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        agent_id (str | Unset):
        analysis_type (str | Unset):
        page (int | Unset):
        page_size (int | Unset):
        order (RoiListAnalysesOrder | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | RoiListAnalysesResult
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            client=client,
            agent_id=agent_id,
            analysis_type=analysis_type,
            page=page,
            page_size=page_size,
            order=order,
        )
    ).parsed
