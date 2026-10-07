from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="SettingsSettingsDescriptionType")


@_attrs_define
class SettingsSettingsDescriptionType:
    """
    Attributes:
        key (str):
        value (str):
        is_organization_key (bool | Unset):
        last_edited (str | Unset):
    """

    key: str
    value: str
    is_organization_key: bool | Unset = UNSET
    last_edited: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        value = self.value

        is_organization_key = self.is_organization_key

        last_edited = self.last_edited

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "value": value,
            }
        )
        if is_organization_key is not UNSET:
            field_dict["is_organization_key"] = is_organization_key
        if last_edited is not UNSET:
            field_dict["last_edited"] = last_edited

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        value = d.pop("value")

        is_organization_key = d.pop("is_organization_key", UNSET)

        last_edited = d.pop("last_edited", UNSET)

        settings_settings_description_type = cls(
            key=key,
            value=value,
            is_organization_key=is_organization_key,
            last_edited=last_edited,
        )

        settings_settings_description_type.additional_properties = d
        return settings_settings_description_type

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
