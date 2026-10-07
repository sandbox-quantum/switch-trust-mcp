from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.gateway_membership import GatewayMembership


T = TypeVar("T", bound="GatewayPaginatedResponseGatewayMembership")


@_attrs_define
class GatewayPaginatedResponseGatewayMembership:
    """
    Attributes:
        data (list[GatewayMembership] | Unset):
        limit (int | Unset):
        offset (int | Unset):
        total (int | Unset):
    """

    data: list[GatewayMembership] | Unset = UNSET
    limit: int | Unset = UNSET
    offset: int | Unset = UNSET
    total: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.gateway_membership import GatewayMembership  # noqa: PLC0415

        data: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

        limit = self.limit

        offset = self.offset

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if limit is not UNSET:
            field_dict["limit"] = limit
        if offset is not UNSET:
            field_dict["offset"] = offset
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gateway_membership import GatewayMembership  # noqa: PLC0415

        d = dict(src_dict)
        _data = d.pop("data", UNSET)
        data: list[GatewayMembership] | Unset = UNSET
        if _data is not UNSET:
            data = []
            for data_item_data in _data:
                data_item = GatewayMembership.from_dict(data_item_data)

                data.append(data_item)

        limit = d.pop("limit", UNSET)

        offset = d.pop("offset", UNSET)

        total = d.pop("total", UNSET)

        gateway_paginated_response_gateway_membership = cls(
            data=data,
            limit=limit,
            offset=offset,
            total=total,
        )

        gateway_paginated_response_gateway_membership.additional_properties = d
        return gateway_paginated_response_gateway_membership

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
