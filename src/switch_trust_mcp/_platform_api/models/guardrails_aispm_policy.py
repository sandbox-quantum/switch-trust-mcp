from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.guardrails_aispm_detectors import GuardrailsAispmDetectors


T = TypeVar("T", bound="GuardrailsAispmPolicy")


@_attrs_define
class GuardrailsAispmPolicy:
    """
    Attributes:
        description (str | Unset):
        detectors (GuardrailsAispmDetectors | Unset):
        name (str | Unset):
    """

    description: str | Unset = UNSET
    detectors: GuardrailsAispmDetectors | Unset = UNSET
    name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.guardrails_aispm_detectors import GuardrailsAispmDetectors  # noqa: PLC0415

        description = self.description

        detectors: dict[str, Any] | Unset = UNSET
        if not isinstance(self.detectors, Unset):
            detectors = self.detectors.to_dict()

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if detectors is not UNSET:
            field_dict["detectors"] = detectors
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.guardrails_aispm_detectors import GuardrailsAispmDetectors  # noqa: PLC0415

        d = dict(src_dict)
        description = d.pop("description", UNSET)

        _detectors = d.pop("detectors", UNSET)
        detectors: GuardrailsAispmDetectors | Unset
        if isinstance(_detectors, Unset):
            detectors = UNSET
        else:
            detectors = GuardrailsAispmDetectors.from_dict(_detectors)

        name = d.pop("name", UNSET)

        guardrails_aispm_policy = cls(
            description=description,
            detectors=detectors,
            name=name,
        )

        guardrails_aispm_policy.additional_properties = d
        return guardrails_aispm_policy

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
