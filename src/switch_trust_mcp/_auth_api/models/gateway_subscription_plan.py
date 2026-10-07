from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="GatewaySubscriptionPlan")


@_attrs_define
class GatewaySubscriptionPlan:
    """
    Attributes:
        cancel_at_period_end (bool | Unset):
        current_period_end (str | Unset):
        tier (str | Unset):
    """

    cancel_at_period_end: bool | Unset = UNSET
    current_period_end: str | Unset = UNSET
    tier: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cancel_at_period_end = self.cancel_at_period_end

        current_period_end = self.current_period_end

        tier = self.tier

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cancel_at_period_end is not UNSET:
            field_dict["cancel_at_period_end"] = cancel_at_period_end
        if current_period_end is not UNSET:
            field_dict["current_period_end"] = current_period_end
        if tier is not UNSET:
            field_dict["tier"] = tier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cancel_at_period_end = d.pop("cancel_at_period_end", UNSET)

        current_period_end = d.pop("current_period_end", UNSET)

        tier = d.pop("tier", UNSET)

        gateway_subscription_plan = cls(
            cancel_at_period_end=cancel_at_period_end,
            current_period_end=current_period_end,
            tier=tier,
        )

        gateway_subscription_plan.additional_properties = d
        return gateway_subscription_plan

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
