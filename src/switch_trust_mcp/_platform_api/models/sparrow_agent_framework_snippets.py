from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="SparrowAgentFrameworkSnippets")


@_attrs_define
class SparrowAgentFrameworkSnippets:
    """
    Attributes:
        code_snippet (str | Unset):
        environment_variables (str | Unset):
        install_snippet (str | Unset):
        key (str | Unset):
        name (str | Unset):
    """

    code_snippet: str | Unset = UNSET
    environment_variables: str | Unset = UNSET
    install_snippet: str | Unset = UNSET
    key: str | Unset = UNSET
    name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code_snippet = self.code_snippet

        environment_variables = self.environment_variables

        install_snippet = self.install_snippet

        key = self.key

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code_snippet is not UNSET:
            field_dict["codeSnippet"] = code_snippet
        if environment_variables is not UNSET:
            field_dict["environmentVariables"] = environment_variables
        if install_snippet is not UNSET:
            field_dict["installSnippet"] = install_snippet
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code_snippet = d.pop("codeSnippet", UNSET)

        environment_variables = d.pop("environmentVariables", UNSET)

        install_snippet = d.pop("installSnippet", UNSET)

        key = d.pop("key", UNSET)

        name = d.pop("name", UNSET)

        sparrow_agent_framework_snippets = cls(
            code_snippet=code_snippet,
            environment_variables=environment_variables,
            install_snippet=install_snippet,
            key=key,
            name=name,
        )

        sparrow_agent_framework_snippets.additional_properties = d
        return sparrow_agent_framework_snippets

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
