from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="ApiManagedAgentStatusResponse")


@_attrs_define
class ApiManagedAgentStatusResponse:
    """
    Attributes:
        count (int | Unset):
        enabled (bool | Unset):
        managed (bool | Unset):
    """

    count: int | Unset = UNSET
    enabled: bool | Unset = UNSET
    managed: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        enabled = self.enabled

        managed = self.managed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if managed is not UNSET:
            field_dict["managed"] = managed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count", UNSET)

        enabled = d.pop("enabled", UNSET)

        managed = d.pop("managed", UNSET)

        api_managed_agent_status_response = cls(
            count=count,
            enabled=enabled,
            managed=managed,
        )

        api_managed_agent_status_response.additional_properties = d
        return api_managed_agent_status_response

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
