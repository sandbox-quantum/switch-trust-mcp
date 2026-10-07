from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="GatewayInvitation")


@_attrs_define
class GatewayInvitation:
    """
    Attributes:
        created_at (str | Unset):
        email (str | Unset):
        expires_at (str | Unset):
        id (str | Unset):
        organization_id (str | Unset):
        role (str | Unset):
        state (str | Unset):
    """

    created_at: str | Unset = UNSET
    email: str | Unset = UNSET
    expires_at: str | Unset = UNSET
    id: str | Unset = UNSET
    organization_id: str | Unset = UNSET
    role: str | Unset = UNSET
    state: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        email = self.email

        expires_at = self.expires_at

        id = self.id

        organization_id = self.organization_id

        role = self.role

        state = self.state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if email is not UNSET:
            field_dict["email"] = email
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if id is not UNSET:
            field_dict["id"] = id
        if organization_id is not UNSET:
            field_dict["organization_id"] = organization_id
        if role is not UNSET:
            field_dict["role"] = role
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = d.pop("created_at", UNSET)

        email = d.pop("email", UNSET)

        expires_at = d.pop("expires_at", UNSET)

        id = d.pop("id", UNSET)

        organization_id = d.pop("organization_id", UNSET)

        role = d.pop("role", UNSET)

        state = d.pop("state", UNSET)

        gateway_invitation = cls(
            created_at=created_at,
            email=email,
            expires_at=expires_at,
            id=id,
            organization_id=organization_id,
            role=role,
            state=state,
        )

        gateway_invitation.additional_properties = d
        return gateway_invitation

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
