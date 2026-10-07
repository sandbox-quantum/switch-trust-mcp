from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="GatewayAPIKeyInfo")


@_attrs_define
class GatewayAPIKeyInfo:
    """
    Attributes:
        created_at (str | Unset):
        expires_at (str | Unset):
        id (str | Unset):
        last_used_at (str | Unset):
        name (str | Unset):
        obfuscated_value (str | Unset):
        owner_email (str | Unset):
        owner_id (str | Unset):
        owner_name (str | Unset):
        owner_type (str | Unset):
        role (str | Unset):
    """

    created_at: str | Unset = UNSET
    expires_at: str | Unset = UNSET
    id: str | Unset = UNSET
    last_used_at: str | Unset = UNSET
    name: str | Unset = UNSET
    obfuscated_value: str | Unset = UNSET
    owner_email: str | Unset = UNSET
    owner_id: str | Unset = UNSET
    owner_name: str | Unset = UNSET
    owner_type: str | Unset = UNSET
    role: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        expires_at = self.expires_at

        id = self.id

        last_used_at = self.last_used_at

        name = self.name

        obfuscated_value = self.obfuscated_value

        owner_email = self.owner_email

        owner_id = self.owner_id

        owner_name = self.owner_name

        owner_type = self.owner_type

        role = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if id is not UNSET:
            field_dict["id"] = id
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at
        if name is not UNSET:
            field_dict["name"] = name
        if obfuscated_value is not UNSET:
            field_dict["obfuscated_value"] = obfuscated_value
        if owner_email is not UNSET:
            field_dict["owner_email"] = owner_email
        if owner_id is not UNSET:
            field_dict["owner_id"] = owner_id
        if owner_name is not UNSET:
            field_dict["owner_name"] = owner_name
        if owner_type is not UNSET:
            field_dict["owner_type"] = owner_type
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = d.pop("created_at", UNSET)

        expires_at = d.pop("expires_at", UNSET)

        id = d.pop("id", UNSET)

        last_used_at = d.pop("last_used_at", UNSET)

        name = d.pop("name", UNSET)

        obfuscated_value = d.pop("obfuscated_value", UNSET)

        owner_email = d.pop("owner_email", UNSET)

        owner_id = d.pop("owner_id", UNSET)

        owner_name = d.pop("owner_name", UNSET)

        owner_type = d.pop("owner_type", UNSET)

        role = d.pop("role", UNSET)

        gateway_api_key_info = cls(
            created_at=created_at,
            expires_at=expires_at,
            id=id,
            last_used_at=last_used_at,
            name=name,
            obfuscated_value=obfuscated_value,
            owner_email=owner_email,
            owner_id=owner_id,
            owner_name=owner_name,
            owner_type=owner_type,
            role=role,
        )

        gateway_api_key_info.additional_properties = d
        return gateway_api_key_info

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
