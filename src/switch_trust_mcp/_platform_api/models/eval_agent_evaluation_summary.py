from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.eval_agent_health import EvalAgentHealth
    from ..models.eval_coverage_entry import EvalCoverageEntry
    from ..models.eval_trend_summary import EvalTrendSummary


T = TypeVar("T", bound="EvalAgentEvaluationSummary")


@_attrs_define
class EvalAgentEvaluationSummary:
    """
    Attributes:
        coverage (list[EvalCoverageEntry] | Unset):
        health (EvalAgentHealth | Unset):
        trend (EvalTrendSummary | Unset):
    """

    coverage: list[EvalCoverageEntry] | Unset = UNSET
    health: EvalAgentHealth | Unset = UNSET
    trend: EvalTrendSummary | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_agent_health import EvalAgentHealth  # noqa: PLC0415
        from ..models.eval_coverage_entry import EvalCoverageEntry  # noqa: PLC0415
        from ..models.eval_trend_summary import EvalTrendSummary  # noqa: PLC0415

        coverage: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.coverage, Unset):
            coverage = []
            for coverage_item_data in self.coverage:
                coverage_item = coverage_item_data.to_dict()
                coverage.append(coverage_item)

        health: dict[str, Any] | Unset = UNSET
        if not isinstance(self.health, Unset):
            health = self.health.to_dict()

        trend: dict[str, Any] | Unset = UNSET
        if not isinstance(self.trend, Unset):
            trend = self.trend.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if coverage is not UNSET:
            field_dict["coverage"] = coverage
        if health is not UNSET:
            field_dict["health"] = health
        if trend is not UNSET:
            field_dict["trend"] = trend

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_agent_health import EvalAgentHealth  # noqa: PLC0415
        from ..models.eval_coverage_entry import EvalCoverageEntry  # noqa: PLC0415
        from ..models.eval_trend_summary import EvalTrendSummary  # noqa: PLC0415

        d = dict(src_dict)
        _coverage = d.pop("coverage", UNSET)
        coverage: list[EvalCoverageEntry] | Unset = UNSET
        if _coverage is not UNSET:
            coverage = []
            for coverage_item_data in _coverage:
                coverage_item = EvalCoverageEntry.from_dict(coverage_item_data)

                coverage.append(coverage_item)

        _health = d.pop("health", UNSET)
        health: EvalAgentHealth | Unset
        if isinstance(_health, Unset):
            health = UNSET
        else:
            health = EvalAgentHealth.from_dict(_health)

        _trend = d.pop("trend", UNSET)
        trend: EvalTrendSummary | Unset
        if isinstance(_trend, Unset):
            trend = UNSET
        else:
            trend = EvalTrendSummary.from_dict(_trend)

        eval_agent_evaluation_summary = cls(
            coverage=coverage,
            health=health,
            trend=trend,
        )

        eval_agent_evaluation_summary.additional_properties = d
        return eval_agent_evaluation_summary

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
