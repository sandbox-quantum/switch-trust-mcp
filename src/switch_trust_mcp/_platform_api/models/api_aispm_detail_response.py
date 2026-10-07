from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.cost_burn_rate import CostBurnRate
    from ..models.cost_cost_history import CostCostHistory
    from ..models.cost_period_cost_per_session import CostPeriodCostPerSession
    from ..models.engine_output_embedded_location_section import (
        EngineOutputEmbeddedLocationSection,
    )
    from ..models.engine_output_embedded_section import EngineOutputEmbeddedSection


T = TypeVar("T", bound="ApiAispmDetailResponse")


@_attrs_define
class ApiAispmDetailResponse:
    """
    Attributes:
        cursor (str):
        header (list[str]):
        rows (list[list[Any]]):
        burn_rate (CostBurnRate | Unset):
        cost_history (CostCostHistory | Unset):
        cost_per_session_history (list[CostPeriodCostPerSession] | Unset):
        input_guardrails (EngineOutputEmbeddedSection | Unset):
        locations (EngineOutputEmbeddedLocationSection | Unset):
        mcp_servers (EngineOutputEmbeddedSection | Unset):
        models (EngineOutputEmbeddedSection | Unset):
        monthly_cap (float | Unset):
        output_guardrails (EngineOutputEmbeddedSection | Unset):
        sub_agents (EngineOutputEmbeddedSection | Unset):
        tools (EngineOutputEmbeddedSection | Unset):
        total (int | Unset):
        total_sampling (float | Unset):
    """

    cursor: str
    header: list[str]
    rows: list[list[Any]]
    burn_rate: CostBurnRate | Unset = UNSET
    cost_history: CostCostHistory | Unset = UNSET
    cost_per_session_history: list[CostPeriodCostPerSession] | Unset = UNSET
    input_guardrails: EngineOutputEmbeddedSection | Unset = UNSET
    locations: EngineOutputEmbeddedLocationSection | Unset = UNSET
    mcp_servers: EngineOutputEmbeddedSection | Unset = UNSET
    models: EngineOutputEmbeddedSection | Unset = UNSET
    monthly_cap: float | Unset = UNSET
    output_guardrails: EngineOutputEmbeddedSection | Unset = UNSET
    sub_agents: EngineOutputEmbeddedSection | Unset = UNSET
    tools: EngineOutputEmbeddedSection | Unset = UNSET
    total: int | Unset = UNSET
    total_sampling: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.cost_burn_rate import CostBurnRate  # noqa: PLC0415
        from ..models.cost_cost_history import CostCostHistory  # noqa: PLC0415
        from ..models.cost_period_cost_per_session import CostPeriodCostPerSession  # noqa: PLC0415
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

        burn_rate: dict[str, Any] | Unset = UNSET
        if not isinstance(self.burn_rate, Unset):
            burn_rate = self.burn_rate.to_dict()

        cost_history: dict[str, Any] | Unset = UNSET
        if not isinstance(self.cost_history, Unset):
            cost_history = self.cost_history.to_dict()

        cost_per_session_history: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.cost_per_session_history, Unset):
            cost_per_session_history = []
            for cost_per_session_history_item_data in self.cost_per_session_history:
                cost_per_session_history_item = (
                    cost_per_session_history_item_data.to_dict()
                )
                cost_per_session_history.append(cost_per_session_history_item)

        input_guardrails: dict[str, Any] | Unset = UNSET
        if not isinstance(self.input_guardrails, Unset):
            input_guardrails = self.input_guardrails.to_dict()

        locations: dict[str, Any] | Unset = UNSET
        if not isinstance(self.locations, Unset):
            locations = self.locations.to_dict()

        mcp_servers: dict[str, Any] | Unset = UNSET
        if not isinstance(self.mcp_servers, Unset):
            mcp_servers = self.mcp_servers.to_dict()

        models: dict[str, Any] | Unset = UNSET
        if not isinstance(self.models, Unset):
            models = self.models.to_dict()

        monthly_cap = self.monthly_cap

        output_guardrails: dict[str, Any] | Unset = UNSET
        if not isinstance(self.output_guardrails, Unset):
            output_guardrails = self.output_guardrails.to_dict()

        sub_agents: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sub_agents, Unset):
            sub_agents = self.sub_agents.to_dict()

        tools: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tools, Unset):
            tools = self.tools.to_dict()

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
        if burn_rate is not UNSET:
            field_dict["burn_rate"] = burn_rate
        if cost_history is not UNSET:
            field_dict["cost_history"] = cost_history
        if cost_per_session_history is not UNSET:
            field_dict["cost_per_session_history"] = cost_per_session_history
        if input_guardrails is not UNSET:
            field_dict["input_guardrails"] = input_guardrails
        if locations is not UNSET:
            field_dict["locations"] = locations
        if mcp_servers is not UNSET:
            field_dict["mcp_servers"] = mcp_servers
        if models is not UNSET:
            field_dict["models"] = models
        if monthly_cap is not UNSET:
            field_dict["monthly_cap"] = monthly_cap
        if output_guardrails is not UNSET:
            field_dict["output_guardrails"] = output_guardrails
        if sub_agents is not UNSET:
            field_dict["sub_agents"] = sub_agents
        if tools is not UNSET:
            field_dict["tools"] = tools
        if total is not UNSET:
            field_dict["total"] = total
        if total_sampling is not UNSET:
            field_dict["total_sampling"] = total_sampling

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cost_burn_rate import CostBurnRate  # noqa: PLC0415
        from ..models.cost_cost_history import CostCostHistory  # noqa: PLC0415
        from ..models.cost_period_cost_per_session import CostPeriodCostPerSession  # noqa: PLC0415
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

        _burn_rate = d.pop("burn_rate", UNSET)
        burn_rate: CostBurnRate | Unset
        if isinstance(_burn_rate, Unset):
            burn_rate = UNSET
        else:
            burn_rate = CostBurnRate.from_dict(_burn_rate)

        _cost_history = d.pop("cost_history", UNSET)
        cost_history: CostCostHistory | Unset
        if isinstance(_cost_history, Unset):
            cost_history = UNSET
        else:
            cost_history = CostCostHistory.from_dict(_cost_history)

        _cost_per_session_history = d.pop("cost_per_session_history", UNSET)
        cost_per_session_history: list[CostPeriodCostPerSession] | Unset = UNSET
        if _cost_per_session_history is not UNSET:
            cost_per_session_history = []
            for cost_per_session_history_item_data in _cost_per_session_history:
                cost_per_session_history_item = CostPeriodCostPerSession.from_dict(
                    cost_per_session_history_item_data
                )

                cost_per_session_history.append(cost_per_session_history_item)

        _input_guardrails = d.pop("input_guardrails", UNSET)
        input_guardrails: EngineOutputEmbeddedSection | Unset
        if isinstance(_input_guardrails, Unset):
            input_guardrails = UNSET
        else:
            input_guardrails = EngineOutputEmbeddedSection.from_dict(_input_guardrails)

        _locations = d.pop("locations", UNSET)
        locations: EngineOutputEmbeddedLocationSection | Unset
        if isinstance(_locations, Unset):
            locations = UNSET
        else:
            locations = EngineOutputEmbeddedLocationSection.from_dict(_locations)

        _mcp_servers = d.pop("mcp_servers", UNSET)
        mcp_servers: EngineOutputEmbeddedSection | Unset
        if isinstance(_mcp_servers, Unset):
            mcp_servers = UNSET
        else:
            mcp_servers = EngineOutputEmbeddedSection.from_dict(_mcp_servers)

        _models = d.pop("models", UNSET)
        models: EngineOutputEmbeddedSection | Unset
        if isinstance(_models, Unset):
            models = UNSET
        else:
            models = EngineOutputEmbeddedSection.from_dict(_models)

        monthly_cap = d.pop("monthly_cap", UNSET)

        _output_guardrails = d.pop("output_guardrails", UNSET)
        output_guardrails: EngineOutputEmbeddedSection | Unset
        if isinstance(_output_guardrails, Unset):
            output_guardrails = UNSET
        else:
            output_guardrails = EngineOutputEmbeddedSection.from_dict(
                _output_guardrails
            )

        _sub_agents = d.pop("sub_agents", UNSET)
        sub_agents: EngineOutputEmbeddedSection | Unset
        if isinstance(_sub_agents, Unset):
            sub_agents = UNSET
        else:
            sub_agents = EngineOutputEmbeddedSection.from_dict(_sub_agents)

        _tools = d.pop("tools", UNSET)
        tools: EngineOutputEmbeddedSection | Unset
        if isinstance(_tools, Unset):
            tools = UNSET
        else:
            tools = EngineOutputEmbeddedSection.from_dict(_tools)

        total = d.pop("total", UNSET)

        total_sampling = d.pop("total_sampling", UNSET)

        api_aispm_detail_response = cls(
            cursor=cursor,
            header=header,
            rows=rows,
            burn_rate=burn_rate,
            cost_history=cost_history,
            cost_per_session_history=cost_per_session_history,
            input_guardrails=input_guardrails,
            locations=locations,
            mcp_servers=mcp_servers,
            models=models,
            monthly_cap=monthly_cap,
            output_guardrails=output_guardrails,
            sub_agents=sub_agents,
            tools=tools,
            total=total,
            total_sampling=total_sampling,
        )

        api_aispm_detail_response.additional_properties = d
        return api_aispm_detail_response

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
