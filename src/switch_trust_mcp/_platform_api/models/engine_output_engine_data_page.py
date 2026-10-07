from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="EngineOutputEngineDataPage")


@_attrs_define
class EngineOutputEngineDataPage:
    """
    Attributes:
        cursor (str):
        header (list[str]):
        rows (list[list[Any]]):
        total (int | Unset):
        total_sampling (float | Unset):
    """

    cursor: str
    header: list[str]
    rows: list[list[Any]]
    total: int | Unset = UNSET
    total_sampling: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cursor = self.cursor

        header = self.header

        rows = []
        for rows_item_data in self.rows:
            rows_item = rows_item_data

            rows.append(rows_item)

        total = self.total

        total_sampling = self.total_sampling

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cursor": cursor,
                "header": header,
                "rows": rows,
            }
        )
        if total is not UNSET:
            field_dict["total"] = total
        if total_sampling is not UNSET:
            field_dict["total_sampling"] = total_sampling

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cursor = d.pop("cursor")

        header = cast(list[str], d.pop("header"))

        rows = []
        _rows = d.pop("rows")
        for rows_item_data in _rows:
            rows_item = cast(list[Any], rows_item_data)

            rows.append(rows_item)

        total = d.pop("total", UNSET)

        total_sampling = d.pop("total_sampling", UNSET)

        engine_output_engine_data_page = cls(
            cursor=cursor,
            header=header,
            rows=rows,
            total=total,
            total_sampling=total_sampling,
        )

        engine_output_engine_data_page.additional_properties = d
        return engine_output_engine_data_page

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
