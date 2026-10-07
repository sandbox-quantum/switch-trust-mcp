from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="ApiManagedAgentsSummaryResponse")


@_attrs_define
class ApiManagedAgentsSummaryResponse:
    """
    Attributes:
        cancel_at_period_end (bool | Unset):
        count (int | Unset):
        current_period_end (str | Unset):
        limit (int | Unset):
        subscription_status (str | Unset):
        tier (str | Unset):
    """

    cancel_at_period_end: bool | Unset = UNSET
    count: int | Unset = UNSET
    current_period_end: str | Unset = UNSET
    limit: int | Unset = UNSET
    subscription_status: str | Unset = UNSET
    tier: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cancel_at_period_end = self.cancel_at_period_end

        count = self.count

        current_period_end = self.current_period_end

        limit = self.limit

        subscription_status = self.subscription_status

        tier = self.tier

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cancel_at_period_end is not UNSET:
            field_dict["cancel_at_period_end"] = cancel_at_period_end
        if count is not UNSET:
            field_dict["count"] = count
        if current_period_end is not UNSET:
            field_dict["current_period_end"] = current_period_end
        if limit is not UNSET:
            field_dict["limit"] = limit
        if subscription_status is not UNSET:
            field_dict["subscription_status"] = subscription_status
        if tier is not UNSET:
            field_dict["tier"] = tier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cancel_at_period_end = d.pop("cancel_at_period_end", UNSET)

        count = d.pop("count", UNSET)

        current_period_end = d.pop("current_period_end", UNSET)

        limit = d.pop("limit", UNSET)

        subscription_status = d.pop("subscription_status", UNSET)

        tier = d.pop("tier", UNSET)

        api_managed_agents_summary_response = cls(
            cancel_at_period_end=cancel_at_period_end,
            count=count,
            current_period_end=current_period_end,
            limit=limit,
            subscription_status=subscription_status,
            tier=tier,
        )

        api_managed_agents_summary_response.additional_properties = d
        return api_managed_agents_summary_response

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
