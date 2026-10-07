from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.api_client_storage_put_request_value import (
        ApiClientStoragePutRequestValue,
    )


T = TypeVar("T", bound="ApiClientStoragePutRequest")


@_attrs_define
class ApiClientStoragePutRequest:
    """
    Attributes:
        value (ApiClientStoragePutRequestValue | Unset):
    """

    value: ApiClientStoragePutRequestValue | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.api_client_storage_put_request_value import (
            ApiClientStoragePutRequestValue,
        )  # noqa: PLC0415

        value: dict[str, Any] | Unset = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_client_storage_put_request_value import (
            ApiClientStoragePutRequestValue,
        )  # noqa: PLC0415

        d = dict(src_dict)
        _value = d.pop("value", UNSET)
        value: ApiClientStoragePutRequestValue | Unset
        if isinstance(_value, Unset):
            value = UNSET
        else:
            value = ApiClientStoragePutRequestValue.from_dict(_value)

        api_client_storage_put_request = cls(
            value=value,
        )

        api_client_storage_put_request.additional_properties = d
        return api_client_storage_put_request

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
