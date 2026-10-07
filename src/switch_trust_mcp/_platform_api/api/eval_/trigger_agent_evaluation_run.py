from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_request_error import CommonRequestError
from ...models.eval_trigger_run_response import EvalTriggerRunResponse
from typing import cast


def _get_kwargs(
    tenant_id: str,
    workspace_id: str,
    agent_evaluation_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/eval/agent-evaluations/tenants/{tenant_id}/workspaces/{workspace_id}/{agent_evaluation_id}/trigger".format(
            tenant_id=quote(str(tenant_id), safe=""),
            workspace_id=quote(str(workspace_id), safe=""),
            agent_evaluation_id=quote(str(agent_evaluation_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonRequestError | EvalTriggerRunResponse | None:
    if response.status_code == 202:
        response_202 = EvalTriggerRunResponse.from_dict(response.json())

        return response_202

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

    if response.status_code == 409:
        response_409 = CommonRequestError.from_dict(response.json())

        return response_409

    if response.status_code == 500:
        response_500 = CommonRequestError.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = CommonRequestError.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CommonRequestError | EvalTriggerRunResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    workspace_id: str,
    agent_evaluation_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[CommonRequestError | EvalTriggerRunResponse]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        agent_evaluation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | EvalTriggerRunResponse]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        agent_evaluation_id=agent_evaluation_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    workspace_id: str,
    agent_evaluation_id: str,
    *,
    client: AuthenticatedClient,
) -> CommonRequestError | EvalTriggerRunResponse | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        agent_evaluation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | EvalTriggerRunResponse
    """

    return sync_detailed(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        agent_evaluation_id=agent_evaluation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    workspace_id: str,
    agent_evaluation_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[CommonRequestError | EvalTriggerRunResponse]:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        agent_evaluation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | EvalTriggerRunResponse]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        agent_evaluation_id=agent_evaluation_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    workspace_id: str,
    agent_evaluation_id: str,
    *,
    client: AuthenticatedClient,
) -> CommonRequestError | EvalTriggerRunResponse | None:
    """
    Args:
        tenant_id (str):
        workspace_id (str):
        agent_evaluation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | EvalTriggerRunResponse
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            agent_evaluation_id=agent_evaluation_id,
            client=client,
        )
    ).parsed
