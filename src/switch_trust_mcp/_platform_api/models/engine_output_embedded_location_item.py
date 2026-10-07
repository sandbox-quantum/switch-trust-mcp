from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.engine_output_embedded_location_item_code_location import (
        EngineOutputEmbeddedLocationItemCodeLocation,
    )


T = TypeVar("T", bound="EngineOutputEmbeddedLocationItem")


@_attrs_define
class EngineOutputEmbeddedLocationItem:
    """
    Attributes:
        code_location (EngineOutputEmbeddedLocationItemCodeLocation | Unset):
        id (str | Unset):
    """

    code_location: EngineOutputEmbeddedLocationItemCodeLocation | Unset = UNSET
    id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.engine_output_embedded_location_item_code_location import (
            EngineOutputEmbeddedLocationItemCodeLocation,
        )  # noqa: PLC0415

        code_location: dict[str, Any] | Unset = UNSET
        if not isinstance(self.code_location, Unset):
            code_location = self.code_location.to_dict()

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code_location is not UNSET:
            field_dict["codeLocation"] = code_location
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.engine_output_embedded_location_item_code_location import (
            EngineOutputEmbeddedLocationItemCodeLocation,
        )  # noqa: PLC0415

        d = dict(src_dict)
        _code_location = d.pop("codeLocation", UNSET)
        code_location: EngineOutputEmbeddedLocationItemCodeLocation | Unset
        if isinstance(_code_location, Unset):
            code_location = UNSET
        else:
            code_location = EngineOutputEmbeddedLocationItemCodeLocation.from_dict(
                _code_location
            )

        id = d.pop("id", UNSET)

        engine_output_embedded_location_item = cls(
            code_location=code_location,
            id=id,
        )

        engine_output_embedded_location_item.additional_properties = d
        return engine_output_embedded_location_item

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
