from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="CostBurnRate")


@_attrs_define
class CostBurnRate:
    """
    Attributes:
        daily_spend_rate (float | Unset):
        days_to_cap (float | Unset):
        status (str | Unset):
    """

    daily_spend_rate: float | Unset = UNSET
    days_to_cap: float | Unset = UNSET
    status: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        daily_spend_rate = self.daily_spend_rate

        days_to_cap = self.days_to_cap

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if daily_spend_rate is not UNSET:
            field_dict["daily_spend_rate"] = daily_spend_rate
        if days_to_cap is not UNSET:
            field_dict["days_to_cap"] = days_to_cap
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        daily_spend_rate = d.pop("daily_spend_rate", UNSET)

        days_to_cap = d.pop("days_to_cap", UNSET)

        status = d.pop("status", UNSET)

        cost_burn_rate = cls(
            daily_spend_rate=daily_spend_rate,
            days_to_cap=days_to_cap,
            status=status,
        )

        cost_burn_rate.additional_properties = d
        return cost_burn_rate

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
