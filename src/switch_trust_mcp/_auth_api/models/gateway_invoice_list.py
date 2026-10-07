from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.gateway_invoice import GatewayInvoice


T = TypeVar("T", bound="GatewayInvoiceList")


@_attrs_define
class GatewayInvoiceList:
    """
    Attributes:
        cursor (str | Unset):
        has_more (bool | Unset):
        invoices (list[GatewayInvoice] | Unset):
    """

    cursor: str | Unset = UNSET
    has_more: bool | Unset = UNSET
    invoices: list[GatewayInvoice] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.gateway_invoice import GatewayInvoice  # noqa: PLC0415

        cursor = self.cursor

        has_more = self.has_more

        invoices: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.invoices, Unset):
            invoices = []
            for invoices_item_data in self.invoices:
                invoices_item = invoices_item_data.to_dict()
                invoices.append(invoices_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cursor is not UNSET:
            field_dict["cursor"] = cursor
        if has_more is not UNSET:
            field_dict["has_more"] = has_more
        if invoices is not UNSET:
            field_dict["invoices"] = invoices

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gateway_invoice import GatewayInvoice  # noqa: PLC0415

        d = dict(src_dict)
        cursor = d.pop("cursor", UNSET)

        has_more = d.pop("has_more", UNSET)

        _invoices = d.pop("invoices", UNSET)
        invoices: list[GatewayInvoice] | Unset = UNSET
        if _invoices is not UNSET:
            invoices = []
            for invoices_item_data in _invoices:
                invoices_item = GatewayInvoice.from_dict(invoices_item_data)

                invoices.append(invoices_item)

        gateway_invoice_list = cls(
            cursor=cursor,
            has_more=has_more,
            invoices=invoices,
        )

        gateway_invoice_list.additional_properties = d
        return gateway_invoice_list

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
