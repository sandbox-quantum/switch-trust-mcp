from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.gateway_key_revoke_error import GatewayKeyRevokeError
    from ..models.gateway_member_role import GatewayMemberRole
    from ..models.gateway_member_user import GatewayMemberUser


T = TypeVar("T", bound="GatewayUpdateMemberRoleResult")


@_attrs_define
class GatewayUpdateMemberRoleResult:
    """
    Attributes:
        created_at (str | Unset):
        id (str | Unset):
        key_failures (list[GatewayKeyRevokeError] | Unset):
        keys_revoked (int | Unset):
        organization_id (str | Unset):
        organization_name (str | Unset):
        role (GatewayMemberRole | Unset):
        status (str | Unset):
        user (GatewayMemberUser | Unset):
        user_id (str | Unset):
    """

    created_at: str | Unset = UNSET
    id: str | Unset = UNSET
    key_failures: list[GatewayKeyRevokeError] | Unset = UNSET
    keys_revoked: int | Unset = UNSET
    organization_id: str | Unset = UNSET
    organization_name: str | Unset = UNSET
    role: GatewayMemberRole | Unset = UNSET
    status: str | Unset = UNSET
    user: GatewayMemberUser | Unset = UNSET
    user_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.gateway_key_revoke_error import GatewayKeyRevokeError  # noqa: PLC0415
        from ..models.gateway_member_role import GatewayMemberRole  # noqa: PLC0415
        from ..models.gateway_member_user import GatewayMemberUser  # noqa: PLC0415

        created_at = self.created_at

        id = self.id

        key_failures: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.key_failures, Unset):
            key_failures = []
            for key_failures_item_data in self.key_failures:
                key_failures_item = key_failures_item_data.to_dict()
                key_failures.append(key_failures_item)

        keys_revoked = self.keys_revoked

        organization_id = self.organization_id

        organization_name = self.organization_name

        role: dict[str, Any] | Unset = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.to_dict()

        status = self.status

        user: dict[str, Any] | Unset = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if key_failures is not UNSET:
            field_dict["key_failures"] = key_failures
        if keys_revoked is not UNSET:
            field_dict["keys_revoked"] = keys_revoked
        if organization_id is not UNSET:
            field_dict["organization_id"] = organization_id
        if organization_name is not UNSET:
            field_dict["organization_name"] = organization_name
        if role is not UNSET:
            field_dict["role"] = role
        if status is not UNSET:
            field_dict["status"] = status
        if user is not UNSET:
            field_dict["user"] = user
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gateway_key_revoke_error import GatewayKeyRevokeError  # noqa: PLC0415
        from ..models.gateway_member_role import GatewayMemberRole  # noqa: PLC0415
        from ..models.gateway_member_user import GatewayMemberUser  # noqa: PLC0415

        d = dict(src_dict)
        created_at = d.pop("created_at", UNSET)

        id = d.pop("id", UNSET)

        _key_failures = d.pop("key_failures", UNSET)
        key_failures: list[GatewayKeyRevokeError] | Unset = UNSET
        if _key_failures is not UNSET:
            key_failures = []
            for key_failures_item_data in _key_failures:
                key_failures_item = GatewayKeyRevokeError.from_dict(
                    key_failures_item_data
                )

                key_failures.append(key_failures_item)

        keys_revoked = d.pop("keys_revoked", UNSET)

        organization_id = d.pop("organization_id", UNSET)

        organization_name = d.pop("organization_name", UNSET)

        _role = d.pop("role", UNSET)
        role: GatewayMemberRole | Unset
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = GatewayMemberRole.from_dict(_role)

        status = d.pop("status", UNSET)

        _user = d.pop("user", UNSET)
        user: GatewayMemberUser | Unset
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = GatewayMemberUser.from_dict(_user)

        user_id = d.pop("user_id", UNSET)

        gateway_update_member_role_result = cls(
            created_at=created_at,
            id=id,
            key_failures=key_failures,
            keys_revoked=keys_revoked,
            organization_id=organization_id,
            organization_name=organization_name,
            role=role,
            status=status,
            user=user,
            user_id=user_id,
        )

        gateway_update_member_role_result.additional_properties = d
        return gateway_update_member_role_result

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
