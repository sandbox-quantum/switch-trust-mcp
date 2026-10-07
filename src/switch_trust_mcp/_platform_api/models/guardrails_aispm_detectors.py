from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.guardrails_aispm_detector_entry import GuardrailsAispmDetectorEntry


T = TypeVar("T", bound="GuardrailsAispmDetectors")


@_attrs_define
class GuardrailsAispmDetectors:
    """
    Attributes:
        assistant (list[GuardrailsAispmDetectorEntry] | Unset):
        user (list[GuardrailsAispmDetectorEntry] | Unset):
    """

    assistant: list[GuardrailsAispmDetectorEntry] | Unset = UNSET
    user: list[GuardrailsAispmDetectorEntry] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.guardrails_aispm_detector_entry import (
            GuardrailsAispmDetectorEntry,
        )  # noqa: PLC0415

        assistant: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.assistant, Unset):
            assistant = []
            for assistant_item_data in self.assistant:
                assistant_item = assistant_item_data.to_dict()
                assistant.append(assistant_item)

        user: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.user, Unset):
            user = []
            for user_item_data in self.user:
                user_item = user_item_data.to_dict()
                user.append(user_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if assistant is not UNSET:
            field_dict["assistant"] = assistant
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.guardrails_aispm_detector_entry import (
            GuardrailsAispmDetectorEntry,
        )  # noqa: PLC0415

        d = dict(src_dict)
        _assistant = d.pop("assistant", UNSET)
        assistant: list[GuardrailsAispmDetectorEntry] | Unset = UNSET
        if _assistant is not UNSET:
            assistant = []
            for assistant_item_data in _assistant:
                assistant_item = GuardrailsAispmDetectorEntry.from_dict(
                    assistant_item_data
                )

                assistant.append(assistant_item)

        _user = d.pop("user", UNSET)
        user: list[GuardrailsAispmDetectorEntry] | Unset = UNSET
        if _user is not UNSET:
            user = []
            for user_item_data in _user:
                user_item = GuardrailsAispmDetectorEntry.from_dict(user_item_data)

                user.append(user_item)

        guardrails_aispm_detectors = cls(
            assistant=assistant,
            user=user,
        )

        guardrails_aispm_detectors.additional_properties = d
        return guardrails_aispm_detectors

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
