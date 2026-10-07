from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="CostModelPricing")


@_attrs_define
class CostModelPricing:
    """
    Attributes:
        cache_read_cost_per_1m_tok (float | Unset):
        cache_write_cost_per_1m_tok (float | Unset):
        default_cache_read_cost_per_1m_tok (float | Unset):
        default_cache_write_cost_per_1m_tok (float | Unset):
        default_input_cost_per_1m_tok (float | Unset):
        default_output_cost_per_1m_tok (float | Unset):
        input_cost_per_1m_tok (float | Unset):
        model_fingerprint (str | Unset):
        model_name (str | Unset):
        model_supplier (str | Unset):
        output_cost_per_1m_tok (float | Unset):
        price_as_of (str | Unset):
        source (str | Unset):
    """

    cache_read_cost_per_1m_tok: float | Unset = UNSET
    cache_write_cost_per_1m_tok: float | Unset = UNSET
    default_cache_read_cost_per_1m_tok: float | Unset = UNSET
    default_cache_write_cost_per_1m_tok: float | Unset = UNSET
    default_input_cost_per_1m_tok: float | Unset = UNSET
    default_output_cost_per_1m_tok: float | Unset = UNSET
    input_cost_per_1m_tok: float | Unset = UNSET
    model_fingerprint: str | Unset = UNSET
    model_name: str | Unset = UNSET
    model_supplier: str | Unset = UNSET
    output_cost_per_1m_tok: float | Unset = UNSET
    price_as_of: str | Unset = UNSET
    source: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cache_read_cost_per_1m_tok = self.cache_read_cost_per_1m_tok

        cache_write_cost_per_1m_tok = self.cache_write_cost_per_1m_tok

        default_cache_read_cost_per_1m_tok = self.default_cache_read_cost_per_1m_tok

        default_cache_write_cost_per_1m_tok = self.default_cache_write_cost_per_1m_tok

        default_input_cost_per_1m_tok = self.default_input_cost_per_1m_tok

        default_output_cost_per_1m_tok = self.default_output_cost_per_1m_tok

        input_cost_per_1m_tok = self.input_cost_per_1m_tok

        model_fingerprint = self.model_fingerprint

        model_name = self.model_name

        model_supplier = self.model_supplier

        output_cost_per_1m_tok = self.output_cost_per_1m_tok

        price_as_of = self.price_as_of

        source = self.source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cache_read_cost_per_1m_tok is not UNSET:
            field_dict["cache_read_cost_per_1m_tok"] = cache_read_cost_per_1m_tok
        if cache_write_cost_per_1m_tok is not UNSET:
            field_dict["cache_write_cost_per_1m_tok"] = cache_write_cost_per_1m_tok
        if default_cache_read_cost_per_1m_tok is not UNSET:
            field_dict["default_cache_read_cost_per_1m_tok"] = (
                default_cache_read_cost_per_1m_tok
            )
        if default_cache_write_cost_per_1m_tok is not UNSET:
            field_dict["default_cache_write_cost_per_1m_tok"] = (
                default_cache_write_cost_per_1m_tok
            )
        if default_input_cost_per_1m_tok is not UNSET:
            field_dict["default_input_cost_per_1m_tok"] = default_input_cost_per_1m_tok
        if default_output_cost_per_1m_tok is not UNSET:
            field_dict["default_output_cost_per_1m_tok"] = (
                default_output_cost_per_1m_tok
            )
        if input_cost_per_1m_tok is not UNSET:
            field_dict["input_cost_per_1m_tok"] = input_cost_per_1m_tok
        if model_fingerprint is not UNSET:
            field_dict["model_fingerprint"] = model_fingerprint
        if model_name is not UNSET:
            field_dict["model_name"] = model_name
        if model_supplier is not UNSET:
            field_dict["model_supplier"] = model_supplier
        if output_cost_per_1m_tok is not UNSET:
            field_dict["output_cost_per_1m_tok"] = output_cost_per_1m_tok
        if price_as_of is not UNSET:
            field_dict["price_as_of"] = price_as_of
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cache_read_cost_per_1m_tok = d.pop("cache_read_cost_per_1m_tok", UNSET)

        cache_write_cost_per_1m_tok = d.pop("cache_write_cost_per_1m_tok", UNSET)

        default_cache_read_cost_per_1m_tok = d.pop(
            "default_cache_read_cost_per_1m_tok", UNSET
        )

        default_cache_write_cost_per_1m_tok = d.pop(
            "default_cache_write_cost_per_1m_tok", UNSET
        )

        default_input_cost_per_1m_tok = d.pop("default_input_cost_per_1m_tok", UNSET)

        default_output_cost_per_1m_tok = d.pop("default_output_cost_per_1m_tok", UNSET)

        input_cost_per_1m_tok = d.pop("input_cost_per_1m_tok", UNSET)

        model_fingerprint = d.pop("model_fingerprint", UNSET)

        model_name = d.pop("model_name", UNSET)

        model_supplier = d.pop("model_supplier", UNSET)

        output_cost_per_1m_tok = d.pop("output_cost_per_1m_tok", UNSET)

        price_as_of = d.pop("price_as_of", UNSET)

        source = d.pop("source", UNSET)

        cost_model_pricing = cls(
            cache_read_cost_per_1m_tok=cache_read_cost_per_1m_tok,
            cache_write_cost_per_1m_tok=cache_write_cost_per_1m_tok,
            default_cache_read_cost_per_1m_tok=default_cache_read_cost_per_1m_tok,
            default_cache_write_cost_per_1m_tok=default_cache_write_cost_per_1m_tok,
            default_input_cost_per_1m_tok=default_input_cost_per_1m_tok,
            default_output_cost_per_1m_tok=default_output_cost_per_1m_tok,
            input_cost_per_1m_tok=input_cost_per_1m_tok,
            model_fingerprint=model_fingerprint,
            model_name=model_name,
            model_supplier=model_supplier,
            output_cost_per_1m_tok=output_cost_per_1m_tok,
            price_as_of=price_as_of,
            source=source,
        )

        cost_model_pricing.additional_properties = d
        return cost_model_pricing

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
