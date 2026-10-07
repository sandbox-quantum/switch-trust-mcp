from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="EngineOutputRuleInfo")


@_attrs_define
class EngineOutputRuleInfo:
    """
    Attributes:
        object_types (list[str] | Unset):
        rule_description (str | Unset):
        rule_id (str | Unset):
        rule_name (str | Unset):
        source (str | Unset):
    """

    object_types: list[str] | Unset = UNSET
    rule_description: str | Unset = UNSET
    rule_id: str | Unset = UNSET
    rule_name: str | Unset = UNSET
    source: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_types: list[str] | Unset = UNSET
        if not isinstance(self.object_types, Unset):
            object_types = self.object_types

        rule_description = self.rule_description

        rule_id = self.rule_id

        rule_name = self.rule_name

        source = self.source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_types is not UNSET:
            field_dict["object_types"] = object_types
        if rule_description is not UNSET:
            field_dict["rule_description"] = rule_description
        if rule_id is not UNSET:
            field_dict["rule_id"] = rule_id
        if rule_name is not UNSET:
            field_dict["rule_name"] = rule_name
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        object_types = cast(list[str], d.pop("object_types", UNSET))

        rule_description = d.pop("rule_description", UNSET)

        rule_id = d.pop("rule_id", UNSET)

        rule_name = d.pop("rule_name", UNSET)

        source = d.pop("source", UNSET)

        engine_output_rule_info = cls(
            object_types=object_types,
            rule_description=rule_description,
            rule_id=rule_id,
            rule_name=rule_name,
            source=source,
        )

        engine_output_rule_info.additional_properties = d
        return engine_output_rule_info

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
