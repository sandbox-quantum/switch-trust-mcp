from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_request_error import CommonRequestError
from ...models.engine_output_aispm_guardrail_categories_response import (
    EngineOutputAispmGuardrailCategoriesResponse,
)
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    tenant_id: str,
    workspace_id: str,
    *,
    start_time: str | Unset = UNSET,
    end_time: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["start_time"] = start_time

    params["end_time"] = end_time

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/aispm-llm-interactions-dash/tenants/{tenant_id}/workspaces/{workspace_id}/categories".format(
            tenant_id=quote(str(tenant_id), safe=""),
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonRequestError | EngineOutputAispmGuardrailCategoriesResponse | None:
    if response.status_code == 200:
        response_200 = EngineOutputAispmGuardrailCategoriesResponse.from_dict(
            response.json()
        )

        return response_200

    if response.status_code == 400:
        response_400 = CommonRequestError.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = CommonRequestError.from_dict(response.json())

        return response_401

    if response.status_code == 500:
        response_500 = CommonRequestError.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CommonRequestError | EngineOutputAispmGuardrailCategoriesResponse]:
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
    start_time: str | Unset = UNSET,
    end_time: str | Unset = UNSET,
) -> Response[CommonRequestError | EngineOutputAispmGuardrailCategoriesResponse]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        start_time (str | Unset):
        end_time (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | EngineOutputAispmGuardrailCategoriesResponse]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        start_time=start_time,
        end_time=end_time,
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
    start_time: str | Unset = UNSET,
    end_time: str | Unset = UNSET,
) -> CommonRequestError | EngineOutputAispmGuardrailCategoriesResponse | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        start_time (str | Unset):
        end_time (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | EngineOutputAispmGuardrailCategoriesResponse
    """

    return sync_detailed(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        client=client,
        start_time=start_time,
        end_time=end_time,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    start_time: str | Unset = UNSET,
    end_time: str | Unset = UNSET,
) -> Response[CommonRequestError | EngineOutputAispmGuardrailCategoriesResponse]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        start_time (str | Unset):
        end_time (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | EngineOutputAispmGuardrailCategoriesResponse]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        start_time=start_time,
        end_time=end_time,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    workspace_id: str,
    *,
    client: AuthenticatedClient,
    start_time: str | Unset = UNSET,
    end_time: str | Unset = UNSET,
) -> CommonRequestError | EngineOutputAispmGuardrailCategoriesResponse | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        start_time (str | Unset):
        end_time (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | EngineOutputAispmGuardrailCategoriesResponse
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            client=client,
            start_time=start_time,
            end_time=end_time,
        )
    ).parsed
