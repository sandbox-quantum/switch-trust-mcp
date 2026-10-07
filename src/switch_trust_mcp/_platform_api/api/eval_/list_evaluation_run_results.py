from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_request_error import CommonRequestError
from ...models.eval_list_evaluation_run_results_result import (
    EvalListEvaluationRunResultsResult,
)
from ...models.list_evaluation_run_results_order import ListEvaluationRunResultsOrder
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    tenant_id: str,
    workspace_id: str,
    evaluation_run_id: str,
    *,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
    order: ListEvaluationRunResultsOrder | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["page"] = page

    params["page_size"] = page_size

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/eval/evaluation-runs/tenants/{tenant_id}/workspaces/{workspace_id}/{evaluation_run_id}/results".format(
            tenant_id=quote(str(tenant_id), safe=""),
            workspace_id=quote(str(workspace_id), safe=""),
            evaluation_run_id=quote(str(evaluation_run_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonRequestError | EvalListEvaluationRunResultsResult | None:
    if response.status_code == 200:
        response_200 = EvalListEvaluationRunResultsResult.from_dict(response.json())

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
) -> Response[CommonRequestError | EvalListEvaluationRunResultsResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    workspace_id: str,
    evaluation_run_id: str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
    order: ListEvaluationRunResultsOrder | Unset = UNSET,
) -> Response[CommonRequestError | EvalListEvaluationRunResultsResult]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        evaluation_run_id (str):
        page (int | Unset):
        page_size (int | Unset):
        order (ListEvaluationRunResultsOrder | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | EvalListEvaluationRunResultsResult]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        evaluation_run_id=evaluation_run_id,
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
    evaluation_run_id: str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
    order: ListEvaluationRunResultsOrder | Unset = UNSET,
) -> CommonRequestError | EvalListEvaluationRunResultsResult | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        evaluation_run_id (str):
        page (int | Unset):
        page_size (int | Unset):
        order (ListEvaluationRunResultsOrder | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | EvalListEvaluationRunResultsResult
    """

    return sync_detailed(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        evaluation_run_id=evaluation_run_id,
        client=client,
        page=page,
        page_size=page_size,
        order=order,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    workspace_id: str,
    evaluation_run_id: str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
    order: ListEvaluationRunResultsOrder | Unset = UNSET,
) -> Response[CommonRequestError | EvalListEvaluationRunResultsResult]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        evaluation_run_id (str):
        page (int | Unset):
        page_size (int | Unset):
        order (ListEvaluationRunResultsOrder | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | EvalListEvaluationRunResultsResult]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        evaluation_run_id=evaluation_run_id,
        page=page,
        page_size=page_size,
        order=order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    workspace_id: str,
    evaluation_run_id: str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    page_size: int | Unset = UNSET,
    order: ListEvaluationRunResultsOrder | Unset = UNSET,
) -> CommonRequestError | EvalListEvaluationRunResultsResult | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        evaluation_run_id (str):
        page (int | Unset):
        page_size (int | Unset):
        order (ListEvaluationRunResultsOrder | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | EvalListEvaluationRunResultsResult
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            evaluation_run_id=evaluation_run_id,
            client=client,
            page=page,
            page_size=page_size,
            order=order,
        )
    ).parsed
