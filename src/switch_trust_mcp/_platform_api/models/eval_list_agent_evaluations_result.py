from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.eval_agent_evaluation_record import EvalAgentEvaluationRecord


T = TypeVar("T", bound="EvalListAgentEvaluationsResult")


@_attrs_define
class EvalListAgentEvaluationsResult:
    """
    Attributes:
        items (list[EvalAgentEvaluationRecord] | Unset):
        page (int | Unset):
        page_size (int | Unset):
        total_count (int | Unset):
        total_pages (int | Unset):
    """

    items: list[EvalAgentEvaluationRecord] | Unset = UNSET
    page: int | Unset = UNSET
    page_size: int | Unset = UNSET
    total_count: int | Unset = UNSET
    total_pages: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_agent_evaluation_record import EvalAgentEvaluationRecord  # noqa: PLC0415

        items: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()
                items.append(items_item)

        page = self.page

        page_size = self.page_size

        total_count = self.total_count

        total_pages = self.total_pages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if items is not UNSET:
            field_dict["items"] = items
        if page is not UNSET:
            field_dict["page"] = page
        if page_size is not UNSET:
            field_dict["page_size"] = page_size
        if total_count is not UNSET:
            field_dict["total_count"] = total_count
        if total_pages is not UNSET:
            field_dict["total_pages"] = total_pages

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_agent_evaluation_record import EvalAgentEvaluationRecord  # noqa: PLC0415

        d = dict(src_dict)
        _items = d.pop("items", UNSET)
        items: list[EvalAgentEvaluationRecord] | Unset = UNSET
        if _items is not UNSET:
            items = []
            for items_item_data in _items:
                items_item = EvalAgentEvaluationRecord.from_dict(items_item_data)

                items.append(items_item)

        page = d.pop("page", UNSET)

        page_size = d.pop("page_size", UNSET)

        total_count = d.pop("total_count", UNSET)

        total_pages = d.pop("total_pages", UNSET)

        eval_list_agent_evaluations_result = cls(
            items=items,
            page=page,
            page_size=page_size,
            total_count=total_count,
            total_pages=total_pages,
        )

        eval_list_agent_evaluations_result.additional_properties = d
        return eval_list_agent_evaluations_result

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
