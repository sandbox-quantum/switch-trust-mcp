from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="CostSpendingSummary")


@_attrs_define
class CostSpendingSummary:
    """
    Attributes:
        healthy (int | Unset):
        near_cap (int | Unset):
        no_cap (int | Unset):
        over_cap (int | Unset):
    """

    healthy: int | Unset = UNSET
    near_cap: int | Unset = UNSET
    no_cap: int | Unset = UNSET
    over_cap: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        healthy = self.healthy

        near_cap = self.near_cap

        no_cap = self.no_cap

        over_cap = self.over_cap

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if healthy is not UNSET:
            field_dict["healthy"] = healthy
        if near_cap is not UNSET:
            field_dict["near_cap"] = near_cap
        if no_cap is not UNSET:
            field_dict["no_cap"] = no_cap
        if over_cap is not UNSET:
            field_dict["over_cap"] = over_cap

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        healthy = d.pop("healthy", UNSET)

        near_cap = d.pop("near_cap", UNSET)

        no_cap = d.pop("no_cap", UNSET)

        over_cap = d.pop("over_cap", UNSET)

        cost_spending_summary = cls(
            healthy=healthy,
            near_cap=near_cap,
            no_cap=no_cap,
            over_cap=over_cap,
        )

        cost_spending_summary.additional_properties = d
        return cost_spending_summary

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
