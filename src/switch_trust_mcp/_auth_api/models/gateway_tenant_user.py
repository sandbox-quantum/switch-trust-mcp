from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.gateway_tenant_user_type import GatewayTenantUserType
from ..types import UNSET, Unset


T = TypeVar("T", bound="GatewayTenantUser")


@_attrs_define
class GatewayTenantUser:
    """
    Attributes:
        created_at (str | Unset):
        email (str | Unset):
        first_name (str | Unset):
        id (str | Unset):
        last_name (str | Unset):
        role (str | Unset):
        status (str | Unset):
        type_ (GatewayTenantUserType | Unset):
        user_id (str | Unset):
    """

    created_at: str | Unset = UNSET
    email: str | Unset = UNSET
    first_name: str | Unset = UNSET
    id: str | Unset = UNSET
    last_name: str | Unset = UNSET
    role: str | Unset = UNSET
    status: str | Unset = UNSET
    type_: GatewayTenantUserType | Unset = UNSET
    user_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        email = self.email

        first_name = self.first_name

        id = self.id

        last_name = self.last_name

        role = self.role

        status = self.status

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if email is not UNSET:
            field_dict["email"] = email
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if id is not UNSET:
            field_dict["id"] = id
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if role is not UNSET:
            field_dict["role"] = role
        if status is not UNSET:
            field_dict["status"] = status
        if type_ is not UNSET:
            field_dict["type"] = type_
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = d.pop("created_at", UNSET)

        email = d.pop("email", UNSET)

        first_name = d.pop("first_name", UNSET)

        id = d.pop("id", UNSET)

        last_name = d.pop("last_name", UNSET)

        role = d.pop("role", UNSET)

        status = d.pop("status", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: GatewayTenantUserType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = GatewayTenantUserType(_type_)

        user_id = d.pop("user_id", UNSET)

        gateway_tenant_user = cls(
            created_at=created_at,
            email=email,
            first_name=first_name,
            id=id,
            last_name=last_name,
            role=role,
            status=status,
            type_=type_,
            user_id=user_id,
        )

        gateway_tenant_user.additional_properties = d
        return gateway_tenant_user

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
