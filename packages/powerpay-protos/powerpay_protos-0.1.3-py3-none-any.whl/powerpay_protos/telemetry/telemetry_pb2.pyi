from google.protobuf import timestamp_pb2 as _timestamp_pb2
from powerpay_protos.telemetry import measurement_pb2 as _measurement_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Telemetry(_message.Message):
    __slots__ = ["timestamp", "device", "measurement"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    device: Device
    measurement: _containers.RepeatedCompositeFieldContainer[_measurement_pb2.Measurement]
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., device: _Optional[_Union[Device, _Mapping]] = ..., measurement: _Optional[_Iterable[_Union[_measurement_pb2.Measurement, _Mapping]]] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ["native_id", "integration_type", "outlet_index", "signal_strength", "signal_noise_ratio", "gateway_id"]
    class IntegrationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        INTEGRATION_TYPE_UNDEFINED: _ClassVar[Device.IntegrationType]
        CHIRPSTACK: _ClassVar[Device.IntegrationType]
        EASEE: _ClassVar[Device.IntegrationType]
    INTEGRATION_TYPE_UNDEFINED: Device.IntegrationType
    CHIRPSTACK: Device.IntegrationType
    EASEE: Device.IntegrationType
    NATIVE_ID_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    OUTLET_INDEX_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NOISE_RATIO_FIELD_NUMBER: _ClassVar[int]
    GATEWAY_ID_FIELD_NUMBER: _ClassVar[int]
    native_id: str
    integration_type: Device.IntegrationType
    outlet_index: int
    signal_strength: float
    signal_noise_ratio: float
    gateway_id: str
    def __init__(self, native_id: _Optional[str] = ..., integration_type: _Optional[_Union[Device.IntegrationType, str]] = ..., outlet_index: _Optional[int] = ..., signal_strength: _Optional[float] = ..., signal_noise_ratio: _Optional[float] = ..., gateway_id: _Optional[str] = ...) -> None: ...
