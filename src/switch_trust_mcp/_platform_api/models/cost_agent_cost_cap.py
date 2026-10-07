from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="CostAgentCostCap")


@_attrs_define
class CostAgentCostCap:
    """
    Attributes:
        agent_id (str | Unset):
        monthly_cap (float | Unset):
    """

    agent_id: str | Unset = UNSET
    monthly_cap: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        monthly_cap = self.monthly_cap

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if monthly_cap is not UNSET:
            field_dict["monthly_cap"] = monthly_cap

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id", UNSET)

        monthly_cap = d.pop("monthly_cap", UNSET)

        cost_agent_cost_cap = cls(
            agent_id=agent_id,
            monthly_cap=monthly_cap,
        )

        cost_agent_cost_cap.additional_properties = d
        return cost_agent_cost_cap

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
