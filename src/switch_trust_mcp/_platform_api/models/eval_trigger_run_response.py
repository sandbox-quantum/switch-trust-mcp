from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="EvalTriggerRunResponse")


@_attrs_define
class EvalTriggerRunResponse:
    """
    Attributes:
        id (str | Unset):
        message (str | Unset):
        run_id (str | Unset):
        run_requested (bool | Unset):
    """

    id: str | Unset = UNSET
    message: str | Unset = UNSET
    run_id: str | Unset = UNSET
    run_requested: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        message = self.message

        run_id = self.run_id

        run_requested = self.run_requested

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if message is not UNSET:
            field_dict["message"] = message
        if run_id is not UNSET:
            field_dict["run_id"] = run_id
        if run_requested is not UNSET:
            field_dict["run_requested"] = run_requested

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        message = d.pop("message", UNSET)

        run_id = d.pop("run_id", UNSET)

        run_requested = d.pop("run_requested", UNSET)

        eval_trigger_run_response = cls(
            id=id,
            message=message,
            run_id=run_id,
            run_requested=run_requested,
        )

        eval_trigger_run_response.additional_properties = d
        return eval_trigger_run_response

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
