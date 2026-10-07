from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_request_error import CommonRequestError
from ...models.cost_list_model_pricing_result import CostListModelPricingResult
from typing import cast


def _get_kwargs(
    tenant_id: str,
    workspace_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/cost/model-pricing/tenants/{tenant_id}/workspaces/{workspace_id}".format(
            tenant_id=quote(str(tenant_id), safe=""),
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonRequestError | CostListModelPricingResult | None:
    if response.status_code == 200:
        response_200 = CostListModelPricingResult.from_dict(response.json())

        return response_200

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
) -> Response[CommonRequestError | CostListModelPricingResult]:
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
) -> Response[CommonRequestError | CostListModelPricingResult]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | CostListModelPricingResult]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
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
) -> CommonRequestError | CostListModelPricingResult | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | CostListModelPricingResult
    """

    return sync_detailed(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    workspace_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[CommonRequestError | CostListModelPricingResult]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | CostListModelPricingResult]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    workspace_id: str,
    *,
    client: AuthenticatedClient,
) -> CommonRequestError | CostListModelPricingResult | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | CostListModelPricingResult
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            client=client,
        )
    ).parsed
