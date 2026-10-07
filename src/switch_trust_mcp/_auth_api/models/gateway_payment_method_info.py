from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="GatewayPaymentMethodInfo")


@_attrs_define
class GatewayPaymentMethodInfo:
    """
    Attributes:
        brand (str | Unset):
        exp_month (int | Unset):
        exp_year (int | Unset):
        has_payment_method (bool | Unset):
        last4 (str | Unset):
        type_ (str | Unset):
    """

    brand: str | Unset = UNSET
    exp_month: int | Unset = UNSET
    exp_year: int | Unset = UNSET
    has_payment_method: bool | Unset = UNSET
    last4: str | Unset = UNSET
    type_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        brand = self.brand

        exp_month = self.exp_month

        exp_year = self.exp_year

        has_payment_method = self.has_payment_method

        last4 = self.last4

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if brand is not UNSET:
            field_dict["brand"] = brand
        if exp_month is not UNSET:
            field_dict["exp_month"] = exp_month
        if exp_year is not UNSET:
            field_dict["exp_year"] = exp_year
        if has_payment_method is not UNSET:
            field_dict["has_payment_method"] = has_payment_method
        if last4 is not UNSET:
            field_dict["last4"] = last4
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        brand = d.pop("brand", UNSET)

        exp_month = d.pop("exp_month", UNSET)

        exp_year = d.pop("exp_year", UNSET)

        has_payment_method = d.pop("has_payment_method", UNSET)

        last4 = d.pop("last4", UNSET)

        type_ = d.pop("type", UNSET)

        gateway_payment_method_info = cls(
            brand=brand,
            exp_month=exp_month,
            exp_year=exp_year,
            has_payment_method=has_payment_method,
            last4=last4,
            type_=type_,
        )

        gateway_payment_method_info.additional_properties = d
        return gateway_payment_method_info

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
