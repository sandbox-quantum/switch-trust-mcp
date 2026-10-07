from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="ApiDisableExcessManagedAgentsResponse")


@_attrs_define
class ApiDisableExcessManagedAgentsResponse:
    """
    Attributes:
        disabled (int | Unset):
        keep (int | Unset):
    """

    disabled: int | Unset = UNSET
    keep: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disabled = self.disabled

        keep = self.keep

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if keep is not UNSET:
            field_dict["keep"] = keep

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        disabled = d.pop("disabled", UNSET)

        keep = d.pop("keep", UNSET)

        api_disable_excess_managed_agents_response = cls(
            disabled=disabled,
            keep=keep,
        )

        api_disable_excess_managed_agents_response.additional_properties = d
        return api_disable_excess_managed_agents_response

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
