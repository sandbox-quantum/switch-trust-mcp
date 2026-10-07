from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_request_error import CommonRequestError
from ...models.get_external_rules_response_200 import GetExternalRulesResponse200
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    *,
    name_ilk: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["name__ilk"] = name_ilk

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/external-rules",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonRequestError | GetExternalRulesResponse200 | None:
    if response.status_code == 200:
        response_200 = GetExternalRulesResponse200.from_dict(response.json())

        return response_200

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
) -> Response[CommonRequestError | GetExternalRulesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    name_ilk: str | Unset = UNSET,
) -> Response[CommonRequestError | GetExternalRulesResponse200]:
    """
    Args:
        name_ilk (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | GetExternalRulesResponse200]
    """

    kwargs = _get_kwargs(
        name_ilk=name_ilk,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    name_ilk: str | Unset = UNSET,
) -> CommonRequestError | GetExternalRulesResponse200 | None:
    """
    Args:
        name_ilk (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | GetExternalRulesResponse200
    """

    return sync_detailed(
        client=client,
        name_ilk=name_ilk,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    name_ilk: str | Unset = UNSET,
) -> Response[CommonRequestError | GetExternalRulesResponse200]:
    """
    Args:
        name_ilk (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonRequestError | GetExternalRulesResponse200]
    """

    kwargs = _get_kwargs(
        name_ilk=name_ilk,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    name_ilk: str | Unset = UNSET,
) -> CommonRequestError | GetExternalRulesResponse200 | None:
    """
    Args:
        name_ilk (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonRequestError | GetExternalRulesResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            name_ilk=name_ilk,
        )
    ).parsed
