from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.sparrow_agent_framework_snippets import SparrowAgentFrameworkSnippets


T = TypeVar("T", bound="SparrowAgentLanguageSnippets")


@_attrs_define
class SparrowAgentLanguageSnippets:
    """
    Attributes:
        available_snippets (list[SparrowAgentFrameworkSnippets] | Unset):
        key (str | Unset):
        nicename (str | Unset):
    """

    available_snippets: list[SparrowAgentFrameworkSnippets] | Unset = UNSET
    key: str | Unset = UNSET
    nicename: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.sparrow_agent_framework_snippets import (
            SparrowAgentFrameworkSnippets,
        )  # noqa: PLC0415

        available_snippets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.available_snippets, Unset):
            available_snippets = []
            for available_snippets_item_data in self.available_snippets:
                available_snippets_item = available_snippets_item_data.to_dict()
                available_snippets.append(available_snippets_item)

        key = self.key

        nicename = self.nicename

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if available_snippets is not UNSET:
            field_dict["availableSnippets"] = available_snippets
        if key is not UNSET:
            field_dict["key"] = key
        if nicename is not UNSET:
            field_dict["nicename"] = nicename

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sparrow_agent_framework_snippets import (
            SparrowAgentFrameworkSnippets,
        )  # noqa: PLC0415

        d = dict(src_dict)
        _available_snippets = d.pop("availableSnippets", UNSET)
        available_snippets: list[SparrowAgentFrameworkSnippets] | Unset = UNSET
        if _available_snippets is not UNSET:
            available_snippets = []
            for available_snippets_item_data in _available_snippets:
                available_snippets_item = SparrowAgentFrameworkSnippets.from_dict(
                    available_snippets_item_data
                )

                available_snippets.append(available_snippets_item)

        key = d.pop("key", UNSET)

        nicename = d.pop("nicename", UNSET)

        sparrow_agent_language_snippets = cls(
            available_snippets=available_snippets,
            key=key,
            nicename=nicename,
        )

        sparrow_agent_language_snippets.additional_properties = d
        return sparrow_agent_language_snippets

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
