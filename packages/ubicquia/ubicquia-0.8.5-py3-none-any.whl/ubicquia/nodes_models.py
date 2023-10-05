from typing import List, Optional, Union

from pydantic import BaseModel, Field
from .base_models import Link, ResponseModel, Base, Meta


class GenericStatus(Base):
    color: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
    value: Optional[Union[str, int]] = None  # value: int
    units: Optional[str] = None
    font_color: Optional[str] = None


class ParentNodes(Base):
    parent_name_L1: Optional[str] = None
    parent_id_L1: Optional[float] = None
    parent_level_L1: Optional[float] = None
    parent_name_L2: Optional[float] = None
    parent_id_L2: Optional[float] = None
    parent_level_L2: Optional[float] = None


class Node(BaseModel):
    id: int
    latitude: Optional[str] = None
    createdate: Optional[str] = None  # yyyy-mm-dd hh:mm:ss
    node: Optional[str] = None
    longitude: Optional[str] = None
    HDOP: Optional[int] = None
    overrideGPS: Optional[int] = None
    deleted: bool
    active: bool
    isActive: bool
    nodetype: Optional[str] = None
    dev_eui: Optional[str] = None  # value
    newnode: Optional[int] = None
    groupId: Optional[int] = None
    poleId: Optional[int] = None
    poleTypeId: Optional[int] = None
    fixtureId: Optional[int] = None
    fixtureTypeId: Optional[int] = None
    imagePath: Optional[str] = None
    CState: Optional[float] = None
    C1State: Optional[float] = None
    VState: Optional[float] = None
    V1State: Optional[float] = None
    nodeTypeId: Optional[int] = None
    twinPole: bool
    poleColor: Optional[str] = None
    poleHeight: Optional[str] = None
    maintenanceCompany: Optional[str] = None
    pole_id: Optional[int] = None
    poleType: Optional[str] = None
    fixture_id: Optional[int] = None
    fixtureType: Optional[str] = None
    dualDim: int
    on_cycles: int
    off_cycles: int
    fixture_cycles: str  # On: 0 Off: 0,
    running_hours: str
    node_events_checked_at: str  # yyyy-mm-dd hh:mm:ss
    updatedAt: str  # yyyy-mm-dd hh:mm:ss
    deactivatedAt: Optional[str] = None
    node_level_type_id: int
    parent_id: Optional[int] = None
    Description: Optional[str] = None
    poleTypeName: Optional[str] = None
    poleTypeCreatedAt: Optional[str] = None  # yyyy-mm-dd hh:mm:ss
    poleTypeUpdatedAt: Optional[str] = None  # yyyy-mm-dd hh:mm:ss
    groupName: Optional[str] = None
    zoneId: Optional[int] = None
    zoneName: Optional[str] = None
    gpsLatitude: Optional[float] = None
    gpsLongitude: Optional[float] = None
    cns_id: int
    nodeState: Optional[str] = None
    versionState: int
    LState: int
    yState: Optional[str] = None
    RqState: Optional[int] = None
    LD1State: int  # dim value
    LD2State: Optional[int] = None
    LPState: int
    LhState: Optional[float] = None
    LThOffState: int
    LthOnState: int
    SState: int
    RaState: Optional[str] = None
    bState: int
    FFState: Optional[int] = None
    BBState: Optional[int] = None
    TTState: int
    VtSagState: int
    VTSwellState: int
    PFState: int
    LFState: int
    yDState: float
    createdDateTime: str  # yyyy-mm-dd hh:mm:ss
    updatedDateTime: str  # yyyy-mm-dd hh:mm:ss
    StrayV: bool
    stray_voltage_status: str
    fixture_wattage: Optional[int] = None
    state: str
    SHState: str
    power: Optional[Union[float, str]] = None
    # custom1: Optional[str]
    # custom2: Optional[str]
    # custom3: Optional[str]
    # custom4: Optional[str]
    # custom5: Optional[str]
    # custom6: Optional[str]
    # custom7: Optional[str]
    # custom8: Optional[str]
    # custom9: Optional[str]
    # custom10: Optional[str]
    # custom11: Optional[str]
    # custom12: Optional[str]
    # custom13: Optional[str]
    # custom14: Optional[str]
    # custom15: Optional[str]
    # custom16: Optional[str]
    # custom17: Optional[str]
    # custom18: Optional[str]
    # custom19: Optional[str]
    # custom20: Optional[str]
    parent_nodes: List[ParentNodes] = None
    temperature_c: Optional[int] = None
    temperature_f: Optional[int] = None
    humidity: Optional[int] = None
    pressure: Optional[int] = None
    pm1_0: Optional[int] = None
    pm2_5: Optional[int] = None
    pm10: Optional[int] = None
    so2: Optional[int] = None
    o3: Optional[int] = None
    co: Optional[int] = None
    no2: Optional[int] = None
    noise_level: Optional[int] = None
    aqi: Optional[int] = None
    primary_pollutant: Optional[str] = None
    aq_updated_date: Optional[str] = None  # mm/dd/yy
    aq_updated_time: Optional[str] = None  # h:s:i A,
    command_status: Optional[str] = None
    light_status: str
    aqi_status: Optional[GenericStatus] = None
    sensor_initialized: bool
    powerFactorState: Optional[float] = None
    ambient_temperature_c: Optional[int] = None
    ambient_temperature_f: Optional[int] = None
    dsState: Optional[int] = None
    circuit_switch: int


class NodeListResponse(ResponseModel):
    # data: Union[List[Node], Node]
    data: List[Node]
    links: Optional[Link] = None
    meta: Optional[Meta] = None


class NodeResponse(ResponseModel):
    data: Node


class DiscoverDeviceData(BaseModel):
    lp_state: int = Field(..., alias='LPState')
    dali: str
    dali_status: str
    dev_eui: str
    id: int
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    updated_date_time: str = Field(..., alias='updatedDateTime')


class DiscoverDeviceMeta(BaseModel):
    all_count: int
    filter_count: int


class DiscoverDevices(ResponseModel):
    data: List[DiscoverDeviceData] = []
    meta: DiscoverDeviceMeta
    timestamp: str
