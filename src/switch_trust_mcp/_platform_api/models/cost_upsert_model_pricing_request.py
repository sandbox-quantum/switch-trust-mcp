from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="CostUpsertModelPricingRequest")


@_attrs_define
class CostUpsertModelPricingRequest:
    """
    Attributes:
        cache_read_cost_per_1m_tok (float | Unset):
        cache_write_cost_per_1m_tok (float | Unset):
        input_cost_per_1m_tok (float | Unset):
        output_cost_per_1m_tok (float | Unset):
        price_as_of (str | Unset):
    """

    cache_read_cost_per_1m_tok: float | Unset = UNSET
    cache_write_cost_per_1m_tok: float | Unset = UNSET
    input_cost_per_1m_tok: float | Unset = UNSET
    output_cost_per_1m_tok: float | Unset = UNSET
    price_as_of: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cache_read_cost_per_1m_tok = self.cache_read_cost_per_1m_tok

        cache_write_cost_per_1m_tok = self.cache_write_cost_per_1m_tok

        input_cost_per_1m_tok = self.input_cost_per_1m_tok

        output_cost_per_1m_tok = self.output_cost_per_1m_tok

        price_as_of = self.price_as_of

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cache_read_cost_per_1m_tok is not UNSET:
            field_dict["cache_read_cost_per_1m_tok"] = cache_read_cost_per_1m_tok
        if cache_write_cost_per_1m_tok is not UNSET:
            field_dict["cache_write_cost_per_1m_tok"] = cache_write_cost_per_1m_tok
        if input_cost_per_1m_tok is not UNSET:
            field_dict["input_cost_per_1m_tok"] = input_cost_per_1m_tok
        if output_cost_per_1m_tok is not UNSET:
            field_dict["output_cost_per_1m_tok"] = output_cost_per_1m_tok
        if price_as_of is not UNSET:
            field_dict["price_as_of"] = price_as_of

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cache_read_cost_per_1m_tok = d.pop("cache_read_cost_per_1m_tok", UNSET)

        cache_write_cost_per_1m_tok = d.pop("cache_write_cost_per_1m_tok", UNSET)

        input_cost_per_1m_tok = d.pop("input_cost_per_1m_tok", UNSET)

        output_cost_per_1m_tok = d.pop("output_cost_per_1m_tok", UNSET)

        price_as_of = d.pop("price_as_of", UNSET)

        cost_upsert_model_pricing_request = cls(
            cache_read_cost_per_1m_tok=cache_read_cost_per_1m_tok,
            cache_write_cost_per_1m_tok=cache_write_cost_per_1m_tok,
            input_cost_per_1m_tok=input_cost_per_1m_tok,
            output_cost_per_1m_tok=output_cost_per_1m_tok,
            price_as_of=price_as_of,
        )

        cost_upsert_model_pricing_request.additional_properties = d
        return cost_upsert_model_pricing_request

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
