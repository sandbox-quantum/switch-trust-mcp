from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="GatewayForceDowngradeResult")


@_attrs_define
class GatewayForceDowngradeResult:
    """
    Attributes:
        disabled (int | Unset):
        enforced (bool | Unset):
        previous_tier (str | Unset):
        subscription_still_live (bool | Unset):
        tier (str | Unset):
    """

    disabled: int | Unset = UNSET
    enforced: bool | Unset = UNSET
    previous_tier: str | Unset = UNSET
    subscription_still_live: bool | Unset = UNSET
    tier: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disabled = self.disabled

        enforced = self.enforced

        previous_tier = self.previous_tier

        subscription_still_live = self.subscription_still_live

        tier = self.tier

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if enforced is not UNSET:
            field_dict["enforced"] = enforced
        if previous_tier is not UNSET:
            field_dict["previous_tier"] = previous_tier
        if subscription_still_live is not UNSET:
            field_dict["subscription_still_live"] = subscription_still_live
        if tier is not UNSET:
            field_dict["tier"] = tier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        disabled = d.pop("disabled", UNSET)

        enforced = d.pop("enforced", UNSET)

        previous_tier = d.pop("previous_tier", UNSET)

        subscription_still_live = d.pop("subscription_still_live", UNSET)

        tier = d.pop("tier", UNSET)

        gateway_force_downgrade_result = cls(
            disabled=disabled,
            enforced=enforced,
            previous_tier=previous_tier,
            subscription_still_live=subscription_still_live,
            tier=tier,
        )

        gateway_force_downgrade_result.additional_properties = d
        return gateway_force_downgrade_result

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
