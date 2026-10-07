from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.engine_output_aispm_guardrail_interactions_bucket_entry import (
        EngineOutputAispmGuardrailInteractionsBucketEntry,
    )


T = TypeVar("T", bound="EngineOutputAispmGuardrailInteractionsBucket")


@_attrs_define
class EngineOutputAispmGuardrailInteractionsBucket:
    """
    Attributes:
        alerted (EngineOutputAispmGuardrailInteractionsBucketEntry | Unset):
        blocked (EngineOutputAispmGuardrailInteractionsBucketEntry | Unset):
        errored (EngineOutputAispmGuardrailInteractionsBucketEntry | Unset):
        ok (EngineOutputAispmGuardrailInteractionsBucketEntry | Unset):
        redacted (EngineOutputAispmGuardrailInteractionsBucketEntry | Unset):
        total (EngineOutputAispmGuardrailInteractionsBucketEntry | Unset):
    """

    alerted: EngineOutputAispmGuardrailInteractionsBucketEntry | Unset = UNSET
    blocked: EngineOutputAispmGuardrailInteractionsBucketEntry | Unset = UNSET
    errored: EngineOutputAispmGuardrailInteractionsBucketEntry | Unset = UNSET
    ok: EngineOutputAispmGuardrailInteractionsBucketEntry | Unset = UNSET
    redacted: EngineOutputAispmGuardrailInteractionsBucketEntry | Unset = UNSET
    total: EngineOutputAispmGuardrailInteractionsBucketEntry | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.engine_output_aispm_guardrail_interactions_bucket_entry import (
            EngineOutputAispmGuardrailInteractionsBucketEntry,
        )  # noqa: PLC0415

        alerted: dict[str, Any] | Unset = UNSET
        if not isinstance(self.alerted, Unset):
            alerted = self.alerted.to_dict()

        blocked: dict[str, Any] | Unset = UNSET
        if not isinstance(self.blocked, Unset):
            blocked = self.blocked.to_dict()

        errored: dict[str, Any] | Unset = UNSET
        if not isinstance(self.errored, Unset):
            errored = self.errored.to_dict()

        ok: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ok, Unset):
            ok = self.ok.to_dict()

        redacted: dict[str, Any] | Unset = UNSET
        if not isinstance(self.redacted, Unset):
            redacted = self.redacted.to_dict()

        total: dict[str, Any] | Unset = UNSET
        if not isinstance(self.total, Unset):
            total = self.total.to_dict()

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
        from ..models.engine_output_aispm_guardrail_interactions_bucket_entry import (
            EngineOutputAispmGuardrailInteractionsBucketEntry,
        )  # noqa: PLC0415

        d = dict(src_dict)
        _alerted = d.pop("alerted", UNSET)
        alerted: EngineOutputAispmGuardrailInteractionsBucketEntry | Unset
        if isinstance(_alerted, Unset):
            alerted = UNSET
        else:
            alerted = EngineOutputAispmGuardrailInteractionsBucketEntry.from_dict(
                _alerted
            )

        _blocked = d.pop("blocked", UNSET)
        blocked: EngineOutputAispmGuardrailInteractionsBucketEntry | Unset
        if isinstance(_blocked, Unset):
            blocked = UNSET
        else:
            blocked = EngineOutputAispmGuardrailInteractionsBucketEntry.from_dict(
                _blocked
            )

        _errored = d.pop("errored", UNSET)
        errored: EngineOutputAispmGuardrailInteractionsBucketEntry | Unset
        if isinstance(_errored, Unset):
            errored = UNSET
        else:
            errored = EngineOutputAispmGuardrailInteractionsBucketEntry.from_dict(
                _errored
            )

        _ok = d.pop("ok", UNSET)
        ok: EngineOutputAispmGuardrailInteractionsBucketEntry | Unset
        if isinstance(_ok, Unset):
            ok = UNSET
        else:
            ok = EngineOutputAispmGuardrailInteractionsBucketEntry.from_dict(_ok)

        _redacted = d.pop("redacted", UNSET)
        redacted: EngineOutputAispmGuardrailInteractionsBucketEntry | Unset
        if isinstance(_redacted, Unset):
            redacted = UNSET
        else:
            redacted = EngineOutputAispmGuardrailInteractionsBucketEntry.from_dict(
                _redacted
            )

        _total = d.pop("total", UNSET)
        total: EngineOutputAispmGuardrailInteractionsBucketEntry | Unset
        if isinstance(_total, Unset):
            total = UNSET
        else:
            total = EngineOutputAispmGuardrailInteractionsBucketEntry.from_dict(_total)

        engine_output_aispm_guardrail_interactions_bucket = cls(
            alerted=alerted,
            blocked=blocked,
            errored=errored,
            ok=ok,
            redacted=redacted,
            total=total,
        )

        engine_output_aispm_guardrail_interactions_bucket.additional_properties = d
        return engine_output_aispm_guardrail_interactions_bucket

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
