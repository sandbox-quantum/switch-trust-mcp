from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.cost_period_cost import CostPeriodCost


T = TypeVar("T", bound="CostCostHistory")


@_attrs_define
class CostCostHistory:
    """
    Attributes:
        current_month (float | Unset):
        current_quarter (float | Unset):
        monthly (list[CostPeriodCost] | Unset):
        ytd (float | Unset):
    """

    current_month: float | Unset = UNSET
    current_quarter: float | Unset = UNSET
    monthly: list[CostPeriodCost] | Unset = UNSET
    ytd: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.cost_period_cost import CostPeriodCost  # noqa: PLC0415

        current_month = self.current_month

        current_quarter = self.current_quarter

        monthly: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.monthly, Unset):
            monthly = []
            for monthly_item_data in self.monthly:
                monthly_item = monthly_item_data.to_dict()
                monthly.append(monthly_item)

        ytd = self.ytd

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if current_month is not UNSET:
            field_dict["current_month"] = current_month
        if current_quarter is not UNSET:
            field_dict["current_quarter"] = current_quarter
        if monthly is not UNSET:
            field_dict["monthly"] = monthly
        if ytd is not UNSET:
            field_dict["ytd"] = ytd

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cost_period_cost import CostPeriodCost  # noqa: PLC0415

        d = dict(src_dict)
        current_month = d.pop("current_month", UNSET)

        current_quarter = d.pop("current_quarter", UNSET)

        _monthly = d.pop("monthly", UNSET)
        monthly: list[CostPeriodCost] | Unset = UNSET
        if _monthly is not UNSET:
            monthly = []
            for monthly_item_data in _monthly:
                monthly_item = CostPeriodCost.from_dict(monthly_item_data)

                monthly.append(monthly_item)

        ytd = d.pop("ytd", UNSET)

        cost_cost_history = cls(
            current_month=current_month,
            current_quarter=current_quarter,
            monthly=monthly,
            ytd=ytd,
        )

        cost_cost_history.additional_properties = d
        return cost_cost_history

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
