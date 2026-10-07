from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.api_dashboard_type_certificate_counts import (
        ApiDashboardTypeCertificateCounts,
    )
    from ..models.api_dashboard_type_key_counts import ApiDashboardTypeKeyCounts
    from ..models.api_dashboard_type_operation_counts import (
        ApiDashboardTypeOperationCounts,
    )


T = TypeVar("T", bound="ApiDashboardType")


@_attrs_define
class ApiDashboardType:
    """
    Attributes:
        apps_scanned (int | Unset):
        apps_scanned_last_week (int | Unset):
        certificate_counts (ApiDashboardTypeCertificateCounts | Unset):
        endpoints_scanned (int | Unset):
        endpoints_scanned_last_week (int | Unset):
        files_scanned (int | Unset):
        files_scanned_last_week (int | Unset):
        images_scanned (int | Unset):
        images_scanned_last_week (int | Unset):
        key_counts (ApiDashboardTypeKeyCounts | Unset):
        networks_scanned (int | Unset):
        networks_scanned_last_week (int | Unset):
        newest_session (str | Unset):
        oldest_session (str | Unset):
        operation_counts (ApiDashboardTypeOperationCounts | Unset):
    """

    apps_scanned: int | Unset = UNSET
    apps_scanned_last_week: int | Unset = UNSET
    certificate_counts: ApiDashboardTypeCertificateCounts | Unset = UNSET
    endpoints_scanned: int | Unset = UNSET
    endpoints_scanned_last_week: int | Unset = UNSET
    files_scanned: int | Unset = UNSET
    files_scanned_last_week: int | Unset = UNSET
    images_scanned: int | Unset = UNSET
    images_scanned_last_week: int | Unset = UNSET
    key_counts: ApiDashboardTypeKeyCounts | Unset = UNSET
    networks_scanned: int | Unset = UNSET
    networks_scanned_last_week: int | Unset = UNSET
    newest_session: str | Unset = UNSET
    oldest_session: str | Unset = UNSET
    operation_counts: ApiDashboardTypeOperationCounts | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.api_dashboard_type_certificate_counts import (
            ApiDashboardTypeCertificateCounts,
        )  # noqa: PLC0415
        from ..models.api_dashboard_type_key_counts import ApiDashboardTypeKeyCounts  # noqa: PLC0415
        from ..models.api_dashboard_type_operation_counts import (
            ApiDashboardTypeOperationCounts,
        )  # noqa: PLC0415

        apps_scanned = self.apps_scanned

        apps_scanned_last_week = self.apps_scanned_last_week

        certificate_counts: dict[str, Any] | Unset = UNSET
        if not isinstance(self.certificate_counts, Unset):
            certificate_counts = self.certificate_counts.to_dict()

        endpoints_scanned = self.endpoints_scanned

        endpoints_scanned_last_week = self.endpoints_scanned_last_week

        files_scanned = self.files_scanned

        files_scanned_last_week = self.files_scanned_last_week

        images_scanned = self.images_scanned

        images_scanned_last_week = self.images_scanned_last_week

        key_counts: dict[str, Any] | Unset = UNSET
        if not isinstance(self.key_counts, Unset):
            key_counts = self.key_counts.to_dict()

        networks_scanned = self.networks_scanned

        networks_scanned_last_week = self.networks_scanned_last_week

        newest_session = self.newest_session

        oldest_session = self.oldest_session

        operation_counts: dict[str, Any] | Unset = UNSET
        if not isinstance(self.operation_counts, Unset):
            operation_counts = self.operation_counts.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if apps_scanned is not UNSET:
            field_dict["apps_scanned"] = apps_scanned
        if apps_scanned_last_week is not UNSET:
            field_dict["apps_scanned_last_week"] = apps_scanned_last_week
        if certificate_counts is not UNSET:
            field_dict["certificate_counts"] = certificate_counts
        if endpoints_scanned is not UNSET:
            field_dict["endpoints_scanned"] = endpoints_scanned
        if endpoints_scanned_last_week is not UNSET:
            field_dict["endpoints_scanned_last_week"] = endpoints_scanned_last_week
        if files_scanned is not UNSET:
            field_dict["files_scanned"] = files_scanned
        if files_scanned_last_week is not UNSET:
            field_dict["files_scanned_last_week"] = files_scanned_last_week
        if images_scanned is not UNSET:
            field_dict["images_scanned"] = images_scanned
        if images_scanned_last_week is not UNSET:
            field_dict["images_scanned_last_week"] = images_scanned_last_week
        if key_counts is not UNSET:
            field_dict["key_counts"] = key_counts
        if networks_scanned is not UNSET:
            field_dict["networks_scanned"] = networks_scanned
        if networks_scanned_last_week is not UNSET:
            field_dict["networks_scanned_last_week"] = networks_scanned_last_week
        if newest_session is not UNSET:
            field_dict["newest_session"] = newest_session
        if oldest_session is not UNSET:
            field_dict["oldest_session"] = oldest_session
        if operation_counts is not UNSET:
            field_dict["operation_counts"] = operation_counts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_dashboard_type_certificate_counts import (
            ApiDashboardTypeCertificateCounts,
        )  # noqa: PLC0415
        from ..models.api_dashboard_type_key_counts import ApiDashboardTypeKeyCounts  # noqa: PLC0415
        from ..models.api_dashboard_type_operation_counts import (
            ApiDashboardTypeOperationCounts,
        )  # noqa: PLC0415

        d = dict(src_dict)
        apps_scanned = d.pop("apps_scanned", UNSET)

        apps_scanned_last_week = d.pop("apps_scanned_last_week", UNSET)

        _certificate_counts = d.pop("certificate_counts", UNSET)
        certificate_counts: ApiDashboardTypeCertificateCounts | Unset
        if isinstance(_certificate_counts, Unset):
            certificate_counts = UNSET
        else:
            certificate_counts = ApiDashboardTypeCertificateCounts.from_dict(
                _certificate_counts
            )

        endpoints_scanned = d.pop("endpoints_scanned", UNSET)

        endpoints_scanned_last_week = d.pop("endpoints_scanned_last_week", UNSET)

        files_scanned = d.pop("files_scanned", UNSET)

        files_scanned_last_week = d.pop("files_scanned_last_week", UNSET)

        images_scanned = d.pop("images_scanned", UNSET)

        images_scanned_last_week = d.pop("images_scanned_last_week", UNSET)

        _key_counts = d.pop("key_counts", UNSET)
        key_counts: ApiDashboardTypeKeyCounts | Unset
        if isinstance(_key_counts, Unset):
            key_counts = UNSET
        else:
            key_counts = ApiDashboardTypeKeyCounts.from_dict(_key_counts)

        networks_scanned = d.pop("networks_scanned", UNSET)

        networks_scanned_last_week = d.pop("networks_scanned_last_week", UNSET)

        newest_session = d.pop("newest_session", UNSET)

        oldest_session = d.pop("oldest_session", UNSET)

        _operation_counts = d.pop("operation_counts", UNSET)
        operation_counts: ApiDashboardTypeOperationCounts | Unset
        if isinstance(_operation_counts, Unset):
            operation_counts = UNSET
        else:
            operation_counts = ApiDashboardTypeOperationCounts.from_dict(
                _operation_counts
            )

        api_dashboard_type = cls(
            apps_scanned=apps_scanned,
            apps_scanned_last_week=apps_scanned_last_week,
            certificate_counts=certificate_counts,
            endpoints_scanned=endpoints_scanned,
            endpoints_scanned_last_week=endpoints_scanned_last_week,
            files_scanned=files_scanned,
            files_scanned_last_week=files_scanned_last_week,
            images_scanned=images_scanned,
            images_scanned_last_week=images_scanned_last_week,
            key_counts=key_counts,
            networks_scanned=networks_scanned,
            networks_scanned_last_week=networks_scanned_last_week,
            newest_session=newest_session,
            oldest_session=oldest_session,
            operation_counts=operation_counts,
        )

        api_dashboard_type.additional_properties = d
        return api_dashboard_type

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
