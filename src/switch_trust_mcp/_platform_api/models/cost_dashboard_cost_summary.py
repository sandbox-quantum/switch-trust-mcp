from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.cost_spending_summary import CostSpendingSummary


T = TypeVar("T", bound="CostDashboardCostSummary")


@_attrs_define
class CostDashboardCostSummary:
    """
    Attributes:
        spending_summary (CostSpendingSummary | Unset):
        total_cost_cap (float | Unset):
        total_mtd_cost (float | Unset):
    """

    spending_summary: CostSpendingSummary | Unset = UNSET
    total_cost_cap: float | Unset = UNSET
    total_mtd_cost: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.cost_spending_summary import CostSpendingSummary  # noqa: PLC0415

        spending_summary: dict[str, Any] | Unset = UNSET
        if not isinstance(self.spending_summary, Unset):
            spending_summary = self.spending_summary.to_dict()

        total_cost_cap = self.total_cost_cap

        total_mtd_cost = self.total_mtd_cost

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if spending_summary is not UNSET:
            field_dict["spending_summary"] = spending_summary
        if total_cost_cap is not UNSET:
            field_dict["total_cost_cap"] = total_cost_cap
        if total_mtd_cost is not UNSET:
            field_dict["total_mtd_cost"] = total_mtd_cost

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cost_spending_summary import CostSpendingSummary  # noqa: PLC0415

        d = dict(src_dict)
        _spending_summary = d.pop("spending_summary", UNSET)
        spending_summary: CostSpendingSummary | Unset
        if isinstance(_spending_summary, Unset):
            spending_summary = UNSET
        else:
            spending_summary = CostSpendingSummary.from_dict(_spending_summary)

        total_cost_cap = d.pop("total_cost_cap", UNSET)

        total_mtd_cost = d.pop("total_mtd_cost", UNSET)

        cost_dashboard_cost_summary = cls(
            spending_summary=spending_summary,
            total_cost_cap=total_cost_cap,
            total_mtd_cost=total_mtd_cost,
        )

        cost_dashboard_cost_summary.additional_properties = d
        return cost_dashboard_cost_summary

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
