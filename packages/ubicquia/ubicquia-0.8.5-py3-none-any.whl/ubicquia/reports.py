from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from .base_models import ResponseModel, Link, Meta
from .base import Endpoint


class ReportType(str, Enum):
    day = "day"
    week = "week"
    month = "month"
    year = "year"


# Data models


class EnergyUsage(BaseModel):
    report_type: ReportType
    unit: str
    total: float


class EnergyUsageResponse(ResponseModel):
    data: EnergyUsage


class ReportChart(BaseModel):
    x_axis: str = Field(..., alias="x-axis")
    y_axis: float = Field(..., alias="y-axis")
    color: str
    interval: str  # dates mm/dd/yy


class ReportChartData(EnergyUsage):
    report: List[ReportChart]


class ReportChartResponse(ResponseModel):
    data: ReportChartData


class KilowattHourData(BaseModel):
    dev_eui: str = Field(..., alias="devEui")
    kwh: float = Field(..., alias="KwH")
    created_date_time: str = Field(..., alias="createdDateTime")


class KilowattHourResponse(ResponseModel):
    data: List[KilowattHourData]
    links: Link
    meta: Meta


# Endpoint methods


class Report(Endpoint):
    def energy_usage(self, report_type: ReportType) -> EnergyUsageResponse:
        """Total energy Usage of all nodes.

        Args:
            report_type: only ReportType values

        Returns:
            Data model: EnergyUsageResponse
        """
        url = self.base_url + "/energyusage"
        params = {"report_type": report_type}
        d = self.session.req("get", url, params=params)
        return EnergyUsageResponse(**d)

    def energy_usage_chart(
        self, date: str, report_type: ReportType
    ) -> ReportChartResponse:
        """Energy Usage chart report.

        Args:
            date: format yyyy-mm-dd
            report_type: only ReportType values
        """
        url = self.base_url + "/energyusageChart"
        params = {"report_type": report_type, "date": date}
        d = self.session.req("get", url, params=params)
        return ReportChartResponse(**d)

    def kilowatt_hour(
        self,
        start_date: str,
        end_date: str,
        id_node: str = None,
        page: int = 1,
        per_page: int = 10,
    ) -> KilowattHourResponse:
        """Listing of kilowatt hour summary

        kilowatt hour usage with several parameters

        Args:
            start_date (str): _description_
            end_date (str): _description_
            id_node: group/zone/node ID
            page:
            per_page:
        """
        url = self.base_url + "/kwhLoad"
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "id": id_node,
            "page": page,
            "per_page": per_page,
        }
        d = self.session.req("get", url, params=params)
        return KilowattHourResponse(**d)
