from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.engine_output_count_results_counts import (
        EngineOutputCountResultsCounts,
    )


T = TypeVar("T", bound="EngineOutputCountResults")


@_attrs_define
class EngineOutputCountResults:
    """
    Attributes:
        counts (EngineOutputCountResultsCounts | Unset):
        total_enriched (int | Unset):
        total_filtered (int | Unset):
    """

    counts: EngineOutputCountResultsCounts | Unset = UNSET
    total_enriched: int | Unset = UNSET
    total_filtered: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.engine_output_count_results_counts import (
            EngineOutputCountResultsCounts,
        )  # noqa: PLC0415

        counts: dict[str, Any] | Unset = UNSET
        if not isinstance(self.counts, Unset):
            counts = self.counts.to_dict()

        total_enriched = self.total_enriched

        total_filtered = self.total_filtered

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if counts is not UNSET:
            field_dict["counts"] = counts
        if total_enriched is not UNSET:
            field_dict["totalEnriched"] = total_enriched
        if total_filtered is not UNSET:
            field_dict["totalFiltered"] = total_filtered

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.engine_output_count_results_counts import (
            EngineOutputCountResultsCounts,
        )  # noqa: PLC0415

        d = dict(src_dict)
        _counts = d.pop("counts", UNSET)
        counts: EngineOutputCountResultsCounts | Unset
        if isinstance(_counts, Unset):
            counts = UNSET
        else:
            counts = EngineOutputCountResultsCounts.from_dict(_counts)

        total_enriched = d.pop("totalEnriched", UNSET)

        total_filtered = d.pop("totalFiltered", UNSET)

        engine_output_count_results = cls(
            counts=counts,
            total_enriched=total_enriched,
            total_filtered=total_filtered,
        )

        engine_output_count_results.additional_properties = d
        return engine_output_count_results

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
