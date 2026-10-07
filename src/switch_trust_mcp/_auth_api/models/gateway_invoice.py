from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="GatewayInvoice")


@_attrs_define
class GatewayInvoice:
    """
    Attributes:
        amount_due (int | Unset):
        amount_paid (int | Unset):
        created (str | Unset):
        currency (str | Unset):
        hosted_invoice_url (str | Unset):
        id (str | Unset):
        invoice_pdf (str | Unset):
        number (str | Unset):
        status (str | Unset):
        total (int | Unset):
    """

    amount_due: int | Unset = UNSET
    amount_paid: int | Unset = UNSET
    created: str | Unset = UNSET
    currency: str | Unset = UNSET
    hosted_invoice_url: str | Unset = UNSET
    id: str | Unset = UNSET
    invoice_pdf: str | Unset = UNSET
    number: str | Unset = UNSET
    status: str | Unset = UNSET
    total: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount_due = self.amount_due

        amount_paid = self.amount_paid

        created = self.created

        currency = self.currency

        hosted_invoice_url = self.hosted_invoice_url

        id = self.id

        invoice_pdf = self.invoice_pdf

        number = self.number

        status = self.status

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount_due is not UNSET:
            field_dict["amount_due"] = amount_due
        if amount_paid is not UNSET:
            field_dict["amount_paid"] = amount_paid
        if created is not UNSET:
            field_dict["created"] = created
        if currency is not UNSET:
            field_dict["currency"] = currency
        if hosted_invoice_url is not UNSET:
            field_dict["hosted_invoice_url"] = hosted_invoice_url
        if id is not UNSET:
            field_dict["id"] = id
        if invoice_pdf is not UNSET:
            field_dict["invoice_pdf"] = invoice_pdf
        if number is not UNSET:
            field_dict["number"] = number
        if status is not UNSET:
            field_dict["status"] = status
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount_due = d.pop("amount_due", UNSET)

        amount_paid = d.pop("amount_paid", UNSET)

        created = d.pop("created", UNSET)

        currency = d.pop("currency", UNSET)

        hosted_invoice_url = d.pop("hosted_invoice_url", UNSET)

        id = d.pop("id", UNSET)

        invoice_pdf = d.pop("invoice_pdf", UNSET)

        number = d.pop("number", UNSET)

        status = d.pop("status", UNSET)

        total = d.pop("total", UNSET)

        gateway_invoice = cls(
            amount_due=amount_due,
            amount_paid=amount_paid,
            created=created,
            currency=currency,
            hosted_invoice_url=hosted_invoice_url,
            id=id,
            invoice_pdf=invoice_pdf,
            number=number,
            status=status,
            total=total,
        )

        gateway_invoice.additional_properties = d
        return gateway_invoice

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
