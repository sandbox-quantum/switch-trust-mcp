from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.engine_output_aispm_guardrail_interaction_counts_response_results import (
        EngineOutputAispmGuardrailInteractionCountsResponseResults,
    )


T = TypeVar("T", bound="EngineOutputAispmGuardrailInteractionCountsResponse")


@_attrs_define
class EngineOutputAispmGuardrailInteractionCountsResponse:
    """
    Attributes:
        alerted (int | Unset):
        blocked (int | Unset):
        errored (int | Unset):
        ok (int | Unset):
        redacted (int | Unset):
        results (EngineOutputAispmGuardrailInteractionCountsResponseResults | Unset):
        total (int | Unset):
    """

    alerted: int | Unset = UNSET
    blocked: int | Unset = UNSET
    errored: int | Unset = UNSET
    ok: int | Unset = UNSET
    redacted: int | Unset = UNSET
    results: EngineOutputAispmGuardrailInteractionCountsResponseResults | Unset = UNSET
    total: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.engine_output_aispm_guardrail_interaction_counts_response_results import (
            EngineOutputAispmGuardrailInteractionCountsResponseResults,
        )  # noqa: PLC0415

        alerted = self.alerted

        blocked = self.blocked

        errored = self.errored

        ok = self.ok

        redacted = self.redacted

        results: dict[str, Any] | Unset = UNSET
        if not isinstance(self.results, Unset):
            results = self.results.to_dict()

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
        if results is not UNSET:
            field_dict["results"] = results
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.engine_output_aispm_guardrail_interaction_counts_response_results import (
            EngineOutputAispmGuardrailInteractionCountsResponseResults,
        )  # noqa: PLC0415

        d = dict(src_dict)
        alerted = d.pop("alerted", UNSET)

        blocked = d.pop("blocked", UNSET)

        errored = d.pop("errored", UNSET)

        ok = d.pop("ok", UNSET)

        redacted = d.pop("redacted", UNSET)

        _results = d.pop("results", UNSET)
        results: EngineOutputAispmGuardrailInteractionCountsResponseResults | Unset
        if isinstance(_results, Unset):
            results = UNSET
        else:
            results = (
                EngineOutputAispmGuardrailInteractionCountsResponseResults.from_dict(
                    _results
                )
            )

        total = d.pop("total", UNSET)

        engine_output_aispm_guardrail_interaction_counts_response = cls(
            alerted=alerted,
            blocked=blocked,
            errored=errored,
            ok=ok,
            redacted=redacted,
            results=results,
            total=total,
        )

        engine_output_aispm_guardrail_interaction_counts_response.additional_properties = d
        return engine_output_aispm_guardrail_interaction_counts_response

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
