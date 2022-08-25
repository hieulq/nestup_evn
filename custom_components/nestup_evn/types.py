from array import ArrayType
from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import ENERGY_KILO_WATT_HOUR

from .const import (
    ID_ECON_PER_DAY,
    ID_ECON_PER_MONTH,
    ID_ECOST_PER_DAY,
    ID_ECOST_PER_MONTH,
    ID_FROM_DATE,
    ID_LATEST_UPDATE,
    ID_TO_DATE,
)


@dataclass
class Entity:
    """Describe the sensor entities."""

    id: str
    friendly_name: str
    entity_class: str
    unit: str
    icon: str
    state_class: SensorStateClass | None


@dataclass
class Area:
    """Describe the supported areas."""

    name: str
    location: str
    evn_login_url: str
    evn_data_request_url: str
    supported: bool
    auth_needed: bool
    pattern: ArrayType


@dataclass
class EVN_NAME:
    """Describe the EVN names."""

    HANOI = "EVNHANOI"
    HCMC = "EVNHCMC"
    NPC = "EVNNPC"
    CPC = "EVNCPC"
    SPC = "EVNSPC"


@dataclass
class EVNRequiredKeysMixin:
    """Mixin for required keys."""

    value_fn: Callable[[Any], float]


@dataclass
class EVNSensorEntityDescription(SensorEntityDescription, EVNRequiredKeysMixin):
    """Describes EVN sensor entity."""


VIETNAM_EVN_AREA = [
    Area(
        EVN_NAME.HCMC,
        "Thành phố Hồ Chí Minh",
        "https://cskh.evnhcmc.vn/Dangnhap/checkLG",
        "https://cskh.evnhcmc.vn/Tracuu/ajax_dienNangTieuThuTheoNgay",
        True,
        True,
        ["PE"],
    ),
    Area(
        EVN_NAME.HANOI,
        "Thủ đô Hà Nội",
        "https://apicskh.evnhanoi.com.vn/connect/token",
        "https://evnhanoi.vn/api/TraCuu/LayChiSoDoXa",
        True,
        True,
        ["PD"],
    ),
    Area(
        EVN_NAME.NPC,
        "Khu vực miền Bắc",
        "(EVNNPC does not need this field)",
        "https://meterindex.enterhub.asia/SLngay",
        True,
        False,
        ["PA", "PH", "PM", "PN"],
    ),
    Area(
        EVN_NAME.SPC,
        "Khu vực miền Nam",
        "(EVNSPC does not need this field)",
        "https://www.cskh.evnspc.vn/TraCuu/TraCuuSanLuongDienTieuThuTrongNgay",
        True,
        False,
        ["PB", "PK"],
    ),
    Area(
        EVN_NAME.CPC,
        "Khu vực miền Trung",
        "NOT_YET_SUPPORTED",
        "NOT_YET_SUPPORTED",
        True,
        True,
        ["PQ", "PC", "PP"],
    ),
]

EVN_SENSORS: tuple[EVNSensorEntityDescription, ...] = (
    EVNSensorEntityDescription(
        key=ID_ECON_PER_DAY,
        name="Chỉ số ngày (mới nhất)",
        icon="mdi:flash-outline",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.ENERGY,
        value_fn=lambda data: data[ID_ECON_PER_DAY],
    ),
    EVNSensorEntityDescription(
        key=ID_ECON_PER_MONTH,
        name="Chỉ số tháng (tạm tính)",
        icon="mdi:flash-outline",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.ENERGY,
        value_fn=lambda data: data[ID_ECON_PER_MONTH],
    ),
    EVNSensorEntityDescription(
        key=ID_ECOST_PER_DAY,
        name="Tiền điện ngày (mới nhất)",
        icon="mdi:cash-multiple",
        native_unit_of_measurement="VNĐ",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data[ID_ECOST_PER_DAY],
    ),
    EVNSensorEntityDescription(
        key=ID_ECOST_PER_MONTH,
        name="Tiền điện tháng (tạm tính)",
        icon="mdi:cash-multiple",
        native_unit_of_measurement="VNĐ",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data[ID_ECOST_PER_MONTH],
    ),
    EVNSensorEntityDescription(
        key=ID_LATEST_UPDATE,
        name="Lần cập nhật cuối",
        icon="mdi:calendar-check",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: data[ID_LATEST_UPDATE],
    ),
    EVNSensorEntityDescription(
        key=ID_FROM_DATE,
        name="Ngày bắt đầu hóa đơn tháng",
        icon="mdi:calendar-clock",
        value_fn=lambda data: data[ID_FROM_DATE],
    ),
    EVNSensorEntityDescription(
        key=ID_TO_DATE,
        name="Ngày mới nhất",
        icon="mdi:calendar-clock",
        value_fn=lambda data: data[ID_TO_DATE],
    ),
)
