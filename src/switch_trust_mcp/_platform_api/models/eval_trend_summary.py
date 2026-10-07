from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.eval_trend_point import EvalTrendPoint


T = TypeVar("T", bound="EvalTrendSummary")


@_attrs_define
class EvalTrendSummary:
    """
    Attributes:
        points (list[EvalTrendPoint] | Unset):
        total_runs (int | Unset):
    """

    points: list[EvalTrendPoint] | Unset = UNSET
    total_runs: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_trend_point import EvalTrendPoint  # noqa: PLC0415

        points: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.points, Unset):
            points = []
            for points_item_data in self.points:
                points_item = points_item_data.to_dict()
                points.append(points_item)

        total_runs = self.total_runs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if points is not UNSET:
            field_dict["points"] = points
        if total_runs is not UNSET:
            field_dict["total_runs"] = total_runs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_trend_point import EvalTrendPoint  # noqa: PLC0415

        d = dict(src_dict)
        _points = d.pop("points", UNSET)
        points: list[EvalTrendPoint] | Unset = UNSET
        if _points is not UNSET:
            points = []
            for points_item_data in _points:
                points_item = EvalTrendPoint.from_dict(points_item_data)

                points.append(points_item)

        total_runs = d.pop("total_runs", UNSET)

        eval_trend_summary = cls(
            points=points,
            total_runs=total_runs,
        )

        eval_trend_summary.additional_properties = d
        return eval_trend_summary

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
