from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.api_identity_config import ApiIdentityConfig
    from ..models.api_remote_logging_config import ApiRemoteLoggingConfig
    from ..models.api_remote_metrics_config import ApiRemoteMetricsConfig


T = TypeVar("T", bound="ApiSensorConfiguration")


@_attrs_define
class ApiSensorConfiguration:
    """
    Attributes:
        identity (ApiIdentityConfig | Unset):
        remote_logging (ApiRemoteLoggingConfig | Unset):
        remote_metrics (ApiRemoteMetricsConfig | Unset):
    """

    identity: ApiIdentityConfig | Unset = UNSET
    remote_logging: ApiRemoteLoggingConfig | Unset = UNSET
    remote_metrics: ApiRemoteMetricsConfig | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.api_identity_config import ApiIdentityConfig  # noqa: PLC0415
        from ..models.api_remote_logging_config import ApiRemoteLoggingConfig  # noqa: PLC0415
        from ..models.api_remote_metrics_config import ApiRemoteMetricsConfig  # noqa: PLC0415

        identity: dict[str, Any] | Unset = UNSET
        if not isinstance(self.identity, Unset):
            identity = self.identity.to_dict()

        remote_logging: dict[str, Any] | Unset = UNSET
        if not isinstance(self.remote_logging, Unset):
            remote_logging = self.remote_logging.to_dict()

        remote_metrics: dict[str, Any] | Unset = UNSET
        if not isinstance(self.remote_metrics, Unset):
            remote_metrics = self.remote_metrics.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if identity is not UNSET:
            field_dict["identity"] = identity
        if remote_logging is not UNSET:
            field_dict["remote_logging"] = remote_logging
        if remote_metrics is not UNSET:
            field_dict["remote_metrics"] = remote_metrics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_identity_config import ApiIdentityConfig  # noqa: PLC0415
        from ..models.api_remote_logging_config import ApiRemoteLoggingConfig  # noqa: PLC0415
        from ..models.api_remote_metrics_config import ApiRemoteMetricsConfig  # noqa: PLC0415

        d = dict(src_dict)
        _identity = d.pop("identity", UNSET)
        identity: ApiIdentityConfig | Unset
        if isinstance(_identity, Unset):
            identity = UNSET
        else:
            identity = ApiIdentityConfig.from_dict(_identity)

        _remote_logging = d.pop("remote_logging", UNSET)
        remote_logging: ApiRemoteLoggingConfig | Unset
        if isinstance(_remote_logging, Unset):
            remote_logging = UNSET
        else:
            remote_logging = ApiRemoteLoggingConfig.from_dict(_remote_logging)

        _remote_metrics = d.pop("remote_metrics", UNSET)
        remote_metrics: ApiRemoteMetricsConfig | Unset
        if isinstance(_remote_metrics, Unset):
            remote_metrics = UNSET
        else:
            remote_metrics = ApiRemoteMetricsConfig.from_dict(_remote_metrics)

        api_sensor_configuration = cls(
            identity=identity,
            remote_logging=remote_logging,
            remote_metrics=remote_metrics,
        )

        api_sensor_configuration.additional_properties = d
        return api_sensor_configuration

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
