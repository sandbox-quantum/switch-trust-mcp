from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.api_managed_agent import ApiManagedAgent


T = TypeVar("T", bound="ApiManagedAgentsResponse")


@_attrs_define
class ApiManagedAgentsResponse:
    """
    Attributes:
        agents (list[ApiManagedAgent] | Unset):
        cursor (str | Unset):
        total (int | Unset):
    """

    agents: list[ApiManagedAgent] | Unset = UNSET
    cursor: str | Unset = UNSET
    total: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.api_managed_agent import ApiManagedAgent  # noqa: PLC0415

        agents: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.agents, Unset):
            agents = []
            for agents_item_data in self.agents:
                agents_item = agents_item_data.to_dict()
                agents.append(agents_item)

        cursor = self.cursor

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agents is not UNSET:
            field_dict["agents"] = agents
        if cursor is not UNSET:
            field_dict["cursor"] = cursor
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_managed_agent import ApiManagedAgent  # noqa: PLC0415

        d = dict(src_dict)
        _agents = d.pop("agents", UNSET)
        agents: list[ApiManagedAgent] | Unset = UNSET
        if _agents is not UNSET:
            agents = []
            for agents_item_data in _agents:
                agents_item = ApiManagedAgent.from_dict(agents_item_data)

                agents.append(agents_item)

        cursor = d.pop("cursor", UNSET)

        total = d.pop("total", UNSET)

        api_managed_agents_response = cls(
            agents=agents,
            cursor=cursor,
            total=total,
        )

        api_managed_agents_response.additional_properties = d
        return api_managed_agents_response

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
