from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.engine_output_embedded_location_section import (
        EngineOutputEmbeddedLocationSection,
    )
    from ..models.engine_output_embedded_section import EngineOutputEmbeddedSection


T = TypeVar("T", bound="ApiAispmMcpServerDetailResponse")


@_attrs_define
class ApiAispmMcpServerDetailResponse:
    """
    Attributes:
        cursor (str):
        header (list[str]):
        rows (list[list[Any]]):
        agents (EngineOutputEmbeddedSection | Unset):
        locations (EngineOutputEmbeddedLocationSection | Unset):
        total (int | Unset):
        total_sampling (float | Unset):
    """

    cursor: str
    header: list[str]
    rows: list[list[Any]]
    agents: EngineOutputEmbeddedSection | Unset = UNSET
    locations: EngineOutputEmbeddedLocationSection | Unset = UNSET
    total: int | Unset = UNSET
    total_sampling: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.engine_output_embedded_location_section import (
            EngineOutputEmbeddedLocationSection,
        )  # noqa: PLC0415
        from ..models.engine_output_embedded_section import EngineOutputEmbeddedSection  # noqa: PLC0415

        cursor = self.cursor

        header = self.header

        rows = []
        for rows_item_data in self.rows:
            rows_item = rows_item_data

            rows.append(rows_item)

        agents: dict[str, Any] | Unset = UNSET
        if not isinstance(self.agents, Unset):
            agents = self.agents.to_dict()

        locations: dict[str, Any] | Unset = UNSET
        if not isinstance(self.locations, Unset):
            locations = self.locations.to_dict()

        total = self.total

        total_sampling = self.total_sampling

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cursor": cursor,
                "header": header,
                "rows": rows,
            }
        )
        if agents is not UNSET:
            field_dict["agents"] = agents
        if locations is not UNSET:
            field_dict["locations"] = locations
        if total is not UNSET:
            field_dict["total"] = total
        if total_sampling is not UNSET:
            field_dict["total_sampling"] = total_sampling

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.engine_output_embedded_location_section import (
            EngineOutputEmbeddedLocationSection,
        )  # noqa: PLC0415
        from ..models.engine_output_embedded_section import EngineOutputEmbeddedSection  # noqa: PLC0415

        d = dict(src_dict)
        cursor = d.pop("cursor")

        header = cast(list[str], d.pop("header"))

        rows = []
        _rows = d.pop("rows")
        for rows_item_data in _rows:
            rows_item = cast(list[Any], rows_item_data)

            rows.append(rows_item)

        _agents = d.pop("agents", UNSET)
        agents: EngineOutputEmbeddedSection | Unset
        if isinstance(_agents, Unset):
            agents = UNSET
        else:
            agents = EngineOutputEmbeddedSection.from_dict(_agents)

        _locations = d.pop("locations", UNSET)
        locations: EngineOutputEmbeddedLocationSection | Unset
        if isinstance(_locations, Unset):
            locations = UNSET
        else:
            locations = EngineOutputEmbeddedLocationSection.from_dict(_locations)

        total = d.pop("total", UNSET)

        total_sampling = d.pop("total_sampling", UNSET)

        api_aispm_mcp_server_detail_response = cls(
            cursor=cursor,
            header=header,
            rows=rows,
            agents=agents,
            locations=locations,
            total=total,
            total_sampling=total_sampling,
        )

        api_aispm_mcp_server_detail_response.additional_properties = d
        return api_aispm_mcp_server_detail_response

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
