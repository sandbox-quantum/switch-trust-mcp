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


T = TypeVar("T", bound="GuardrailsAispmPolicyRecord")


@_attrs_define
class GuardrailsAispmPolicyRecord:
    """
    Attributes:
        created_at (str | Unset):
        description (str | Unset):
        detectors (GuardrailsAispmDetectors | Unset):
        id (str | Unset):
        name (str | Unset):
        updated_at (str | Unset):
    """

    created_at: str | Unset = UNSET
    description: str | Unset = UNSET
    detectors: GuardrailsAispmDetectors | Unset = UNSET
    id: str | Unset = UNSET
    name: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.guardrails_aispm_detectors import GuardrailsAispmDetectors  # noqa: PLC0415

        created_at = self.created_at

        description = self.description

        detectors: dict[str, Any] | Unset = UNSET
        if not isinstance(self.detectors, Unset):
            detectors = self.detectors.to_dict()

        id = self.id

        name = self.name

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if description is not UNSET:
            field_dict["description"] = description
        if detectors is not UNSET:
            field_dict["detectors"] = detectors
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.guardrails_aispm_detectors import GuardrailsAispmDetectors  # noqa: PLC0415

        d = dict(src_dict)
        created_at = d.pop("created_at", UNSET)

        description = d.pop("description", UNSET)

        _detectors = d.pop("detectors", UNSET)
        detectors: GuardrailsAispmDetectors | Unset
        if isinstance(_detectors, Unset):
            detectors = UNSET
        else:
            detectors = GuardrailsAispmDetectors.from_dict(_detectors)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        guardrails_aispm_policy_record = cls(
            created_at=created_at,
            description=description,
            detectors=detectors,
            id=id,
            name=name,
            updated_at=updated_at,
        )

        guardrails_aispm_policy_record.additional_properties = d
        return guardrails_aispm_policy_record

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
