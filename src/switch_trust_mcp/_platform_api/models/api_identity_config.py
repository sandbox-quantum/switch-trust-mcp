from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="ApiIdentityConfig")


@_attrs_define
class ApiIdentityConfig:
    """
    Attributes:
        key_scope (str | Unset):
        org_id (str | Unset):
        tenant_id (str | Unset):
        user_id (str | Unset):
        workspace_id (str | Unset):
    """

    key_scope: str | Unset = UNSET
    org_id: str | Unset = UNSET
    tenant_id: str | Unset = UNSET
    user_id: str | Unset = UNSET
    workspace_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key_scope = self.key_scope

        org_id = self.org_id

        tenant_id = self.tenant_id

        user_id = self.user_id

        workspace_id = self.workspace_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key_scope is not UNSET:
            field_dict["key_scope"] = key_scope
        if org_id is not UNSET:
            field_dict["org_id"] = org_id
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key_scope = d.pop("key_scope", UNSET)

        org_id = d.pop("org_id", UNSET)

        tenant_id = d.pop("tenant_id", UNSET)

        user_id = d.pop("user_id", UNSET)

        workspace_id = d.pop("workspace_id", UNSET)

        api_identity_config = cls(
            key_scope=key_scope,
            org_id=org_id,
            tenant_id=tenant_id,
            user_id=user_id,
            workspace_id=workspace_id,
        )

        api_identity_config.additional_properties = d
        return api_identity_config

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
