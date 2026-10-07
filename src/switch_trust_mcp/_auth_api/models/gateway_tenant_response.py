from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.gateway_tenant_response_metadata import GatewayTenantResponseMetadata


T = TypeVar("T", bound="GatewayTenantResponse")


@_attrs_define
class GatewayTenantResponse:
    """
    Attributes:
        created_at (str | Unset):
        created_by (str | Unset):
        id (str | Unset):
        metadata (GatewayTenantResponseMetadata | Unset):
        name (str | Unset):
        updated_at (str | Unset):
    """

    created_at: str | Unset = UNSET
    created_by: str | Unset = UNSET
    id: str | Unset = UNSET
    metadata: GatewayTenantResponseMetadata | Unset = UNSET
    name: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.gateway_tenant_response_metadata import (
            GatewayTenantResponseMetadata,
        )  # noqa: PLC0415

        created_at = self.created_at

        created_by = self.created_by

        id = self.id

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        name = self.name

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if id is not UNSET:
            field_dict["id"] = id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if name is not UNSET:
            field_dict["name"] = name
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gateway_tenant_response_metadata import (
            GatewayTenantResponseMetadata,
        )  # noqa: PLC0415

        d = dict(src_dict)
        created_at = d.pop("created_at", UNSET)

        created_by = d.pop("created_by", UNSET)

        id = d.pop("id", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: GatewayTenantResponseMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = GatewayTenantResponseMetadata.from_dict(_metadata)

        name = d.pop("name", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        gateway_tenant_response = cls(
            created_at=created_at,
            created_by=created_by,
            id=id,
            metadata=metadata,
            name=name,
            updated_at=updated_at,
        )

        gateway_tenant_response.additional_properties = d
        return gateway_tenant_response

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
