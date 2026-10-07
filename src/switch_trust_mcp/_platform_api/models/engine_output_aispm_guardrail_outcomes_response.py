from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="EngineOutputAispmGuardrailOutcomesResponse")


@_attrs_define
class EngineOutputAispmGuardrailOutcomesResponse:
    """
    Attributes:
        alerted (int | Unset):
        blocked (int | Unset):
        errored (int | Unset):
        ok (int | Unset):
        redacted (int | Unset):
        total (int | Unset):
    """

    alerted: int | Unset = UNSET
    blocked: int | Unset = UNSET
    errored: int | Unset = UNSET
    ok: int | Unset = UNSET
    redacted: int | Unset = UNSET
    total: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alerted = self.alerted

        blocked = self.blocked

        errored = self.errored

        ok = self.ok

        redacted = self.redacted

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if alerted is not UNSET:
            field_dict["alerted"] = alerted
        if blocked is not UNSET:
            field_dict["blocked"] = blocked
        if errored is not UNSET:
            field_dict["errored"] = errored
        if ok is not UNSET:
            field_dict["ok"] = ok
        if redacted is not UNSET:
            field_dict["redacted"] = redacted
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        alerted = d.pop("alerted", UNSET)

        blocked = d.pop("blocked", UNSET)

        errored = d.pop("errored", UNSET)

        ok = d.pop("ok", UNSET)

        redacted = d.pop("redacted", UNSET)

        total = d.pop("total", UNSET)

        engine_output_aispm_guardrail_outcomes_response = cls(
            alerted=alerted,
            blocked=blocked,
            errored=errored,
            ok=ok,
            redacted=redacted,
            total=total,
        )

        engine_output_aispm_guardrail_outcomes_response.additional_properties = d
        return engine_output_aispm_guardrail_outcomes_response

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
