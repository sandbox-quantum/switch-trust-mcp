from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.guardrails_aispm_detector_entry_args import (
        GuardrailsAispmDetectorEntryArgs,
    )


T = TypeVar("T", bound="GuardrailsAispmDetectorEntry")


@_attrs_define
class GuardrailsAispmDetectorEntry:
    """
    Attributes:
        action (str | Unset):
        args (GuardrailsAispmDetectorEntryArgs | Unset):
        custom_name (str | Unset):
        severity (str | Unset):
        type_ (str | Unset):
    """

    action: str | Unset = UNSET
    args: GuardrailsAispmDetectorEntryArgs | Unset = UNSET
    custom_name: str | Unset = UNSET
    severity: str | Unset = UNSET
    type_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.guardrails_aispm_detector_entry_args import (
            GuardrailsAispmDetectorEntryArgs,
        )  # noqa: PLC0415

        action = self.action

        args: dict[str, Any] | Unset = UNSET
        if not isinstance(self.args, Unset):
            args = self.args.to_dict()

        custom_name = self.custom_name

        severity = self.severity

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action is not UNSET:
            field_dict["action"] = action
        if args is not UNSET:
            field_dict["args"] = args
        if custom_name is not UNSET:
            field_dict["custom_name"] = custom_name
        if severity is not UNSET:
            field_dict["severity"] = severity
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.guardrails_aispm_detector_entry_args import (
            GuardrailsAispmDetectorEntryArgs,
        )  # noqa: PLC0415

        d = dict(src_dict)
        action = d.pop("action", UNSET)

        _args = d.pop("args", UNSET)
        args: GuardrailsAispmDetectorEntryArgs | Unset
        if isinstance(_args, Unset):
            args = UNSET
        else:
            args = GuardrailsAispmDetectorEntryArgs.from_dict(_args)

        custom_name = d.pop("custom_name", UNSET)

        severity = d.pop("severity", UNSET)

        type_ = d.pop("type", UNSET)

        guardrails_aispm_detector_entry = cls(
            action=action,
            args=args,
            custom_name=custom_name,
            severity=severity,
            type_=type_,
        )

        guardrails_aispm_detector_entry.additional_properties = d
        return guardrails_aispm_detector_entry

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
