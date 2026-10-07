from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.eval_agent_endpoint_config import EvalAgentEndpointConfig
    from ..models.eval_agent_endpoint_endpoint_headers import (
        EvalAgentEndpointEndpointHeaders,
    )


T = TypeVar("T", bound="EvalAgentEndpoint")


@_attrs_define
class EvalAgentEndpoint:
    """
    Attributes:
        config (EvalAgentEndpointConfig | Unset):
        endpoint_auth_type (str | Unset):
        endpoint_credential (str | Unset):
        endpoint_headers (EvalAgentEndpointEndpointHeaders | Unset):
        endpoint_url (str | Unset):
        model_type (str | Unset):
    """

    config: EvalAgentEndpointConfig | Unset = UNSET
    endpoint_auth_type: str | Unset = UNSET
    endpoint_credential: str | Unset = UNSET
    endpoint_headers: EvalAgentEndpointEndpointHeaders | Unset = UNSET
    endpoint_url: str | Unset = UNSET
    model_type: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_agent_endpoint_config import EvalAgentEndpointConfig  # noqa: PLC0415
        from ..models.eval_agent_endpoint_endpoint_headers import (
            EvalAgentEndpointEndpointHeaders,
        )  # noqa: PLC0415

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        endpoint_auth_type = self.endpoint_auth_type

        endpoint_credential = self.endpoint_credential

        endpoint_headers: dict[str, Any] | Unset = UNSET
        if not isinstance(self.endpoint_headers, Unset):
            endpoint_headers = self.endpoint_headers.to_dict()

        endpoint_url = self.endpoint_url

        model_type = self.model_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if endpoint_auth_type is not UNSET:
            field_dict["endpoint_auth_type"] = endpoint_auth_type
        if endpoint_credential is not UNSET:
            field_dict["endpoint_credential"] = endpoint_credential
        if endpoint_headers is not UNSET:
            field_dict["endpoint_headers"] = endpoint_headers
        if endpoint_url is not UNSET:
            field_dict["endpoint_url"] = endpoint_url
        if model_type is not UNSET:
            field_dict["model_type"] = model_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_agent_endpoint_config import EvalAgentEndpointConfig  # noqa: PLC0415
        from ..models.eval_agent_endpoint_endpoint_headers import (
            EvalAgentEndpointEndpointHeaders,
        )  # noqa: PLC0415

        d = dict(src_dict)
        _config = d.pop("config", UNSET)
        config: EvalAgentEndpointConfig | Unset
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = EvalAgentEndpointConfig.from_dict(_config)

        endpoint_auth_type = d.pop("endpoint_auth_type", UNSET)

        endpoint_credential = d.pop("endpoint_credential", UNSET)

        _endpoint_headers = d.pop("endpoint_headers", UNSET)
        endpoint_headers: EvalAgentEndpointEndpointHeaders | Unset
        if isinstance(_endpoint_headers, Unset):
            endpoint_headers = UNSET
        else:
            endpoint_headers = EvalAgentEndpointEndpointHeaders.from_dict(
                _endpoint_headers
            )

        endpoint_url = d.pop("endpoint_url", UNSET)

        model_type = d.pop("model_type", UNSET)

        eval_agent_endpoint = cls(
            config=config,
            endpoint_auth_type=endpoint_auth_type,
            endpoint_credential=endpoint_credential,
            endpoint_headers=endpoint_headers,
            endpoint_url=endpoint_url,
            model_type=model_type,
        )

        eval_agent_endpoint.additional_properties = d
        return eval_agent_endpoint

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
