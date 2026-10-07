from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="EvalCoverageEntry")


@_attrs_define
class EvalCoverageEntry:
    """
    Attributes:
        at_risk (int | Unset):
        code (str | Unset):
        not_run (int | Unset):
        passing (int | Unset):
        total (int | Unset):
    """

    at_risk: int | Unset = UNSET
    code: str | Unset = UNSET
    not_run: int | Unset = UNSET
    passing: int | Unset = UNSET
    total: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at_risk = self.at_risk

        code = self.code

        not_run = self.not_run

        passing = self.passing

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if at_risk is not UNSET:
            field_dict["at_risk"] = at_risk
        if code is not UNSET:
            field_dict["code"] = code
        if not_run is not UNSET:
            field_dict["not_run"] = not_run
        if passing is not UNSET:
            field_dict["passing"] = passing
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        at_risk = d.pop("at_risk", UNSET)

        code = d.pop("code", UNSET)

        not_run = d.pop("not_run", UNSET)

        passing = d.pop("passing", UNSET)

        total = d.pop("total", UNSET)

        eval_coverage_entry = cls(
            at_risk=at_risk,
            code=code,
            not_run=not_run,
            passing=passing,
            total=total,
        )

        eval_coverage_entry.additional_properties = d
        return eval_coverage_entry

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
