from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.eval_agent_endpoint_record_config import EvalAgentEndpointRecordConfig
    from ..models.eval_agent_endpoint_record_endpoint_headers import (
        EvalAgentEndpointRecordEndpointHeaders,
    )


T = TypeVar("T", bound="EvalAgentEndpointRecord")


@_attrs_define
class EvalAgentEndpointRecord:
    """
    Attributes:
        agent_id (str | Unset):
        config (EvalAgentEndpointRecordConfig | Unset):
        created_at (str | Unset):
        endpoint_auth_type (str | Unset):
        endpoint_credential (str | Unset):
        endpoint_headers (EvalAgentEndpointRecordEndpointHeaders | Unset):
        endpoint_url (str | Unset):
        model_type (str | Unset):
        updated_at (str | Unset):
    """

    agent_id: str | Unset = UNSET
    config: EvalAgentEndpointRecordConfig | Unset = UNSET
    created_at: str | Unset = UNSET
    endpoint_auth_type: str | Unset = UNSET
    endpoint_credential: str | Unset = UNSET
    endpoint_headers: EvalAgentEndpointRecordEndpointHeaders | Unset = UNSET
    endpoint_url: str | Unset = UNSET
    model_type: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_agent_endpoint_record_config import (
            EvalAgentEndpointRecordConfig,
        )  # noqa: PLC0415
        from ..models.eval_agent_endpoint_record_endpoint_headers import (
            EvalAgentEndpointRecordEndpointHeaders,
        )  # noqa: PLC0415

        agent_id = self.agent_id

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        created_at = self.created_at

        endpoint_auth_type = self.endpoint_auth_type

        endpoint_credential = self.endpoint_credential

        endpoint_headers: dict[str, Any] | Unset = UNSET
        if not isinstance(self.endpoint_headers, Unset):
            endpoint_headers = self.endpoint_headers.to_dict()

        endpoint_url = self.endpoint_url

        model_type = self.model_type

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if config is not UNSET:
            field_dict["config"] = config
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
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
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_agent_endpoint_record_config import (
            EvalAgentEndpointRecordConfig,
        )  # noqa: PLC0415
        from ..models.eval_agent_endpoint_record_endpoint_headers import (
            EvalAgentEndpointRecordEndpointHeaders,
        )  # noqa: PLC0415

        d = dict(src_dict)
        agent_id = d.pop("agent_id", UNSET)

        _config = d.pop("config", UNSET)
        config: EvalAgentEndpointRecordConfig | Unset
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = EvalAgentEndpointRecordConfig.from_dict(_config)

        created_at = d.pop("created_at", UNSET)

        endpoint_auth_type = d.pop("endpoint_auth_type", UNSET)

        endpoint_credential = d.pop("endpoint_credential", UNSET)

        _endpoint_headers = d.pop("endpoint_headers", UNSET)
        endpoint_headers: EvalAgentEndpointRecordEndpointHeaders | Unset
        if isinstance(_endpoint_headers, Unset):
            endpoint_headers = UNSET
        else:
            endpoint_headers = EvalAgentEndpointRecordEndpointHeaders.from_dict(
                _endpoint_headers
            )

        endpoint_url = d.pop("endpoint_url", UNSET)

        model_type = d.pop("model_type", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        eval_agent_endpoint_record = cls(
            agent_id=agent_id,
            config=config,
            created_at=created_at,
            endpoint_auth_type=endpoint_auth_type,
            endpoint_credential=endpoint_credential,
            endpoint_headers=endpoint_headers,
            endpoint_url=endpoint_url,
            model_type=model_type,
            updated_at=updated_at,
        )

        eval_agent_endpoint_record.additional_properties = d
        return eval_agent_endpoint_record

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
