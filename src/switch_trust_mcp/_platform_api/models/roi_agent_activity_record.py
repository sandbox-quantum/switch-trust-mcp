from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="RoiAgentActivityRecord")


@_attrs_define
class RoiAgentActivityRecord:
    """
    Attributes:
        agent_id (str | Unset):
        interaction_count (int | Unset):
        latest_interaction_time (str | Unset):
    """

    agent_id: str | Unset = UNSET
    interaction_count: int | Unset = UNSET
    latest_interaction_time: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        interaction_count = self.interaction_count

        latest_interaction_time = self.latest_interaction_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if interaction_count is not UNSET:
            field_dict["interaction_count"] = interaction_count
        if latest_interaction_time is not UNSET:
            field_dict["latest_interaction_time"] = latest_interaction_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id", UNSET)

        interaction_count = d.pop("interaction_count", UNSET)

        latest_interaction_time = d.pop("latest_interaction_time", UNSET)

        roi_agent_activity_record = cls(
            agent_id=agent_id,
            interaction_count=interaction_count,
            latest_interaction_time=latest_interaction_time,
        )

        roi_agent_activity_record.additional_properties = d
        return roi_agent_activity_record

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
