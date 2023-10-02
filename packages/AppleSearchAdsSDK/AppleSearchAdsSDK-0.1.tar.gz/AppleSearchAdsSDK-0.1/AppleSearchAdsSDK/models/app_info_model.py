# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : app_info_model
# Time       ：2023/9/4 19:02
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from dataclasses import dataclass
from typing import List


@dataclass
class AppInfoModel:
    adam_id: int
    app_name: str
    country_or_region_codes: List
    developer_name: str

    @classmethod
    def from_apple_dict(cls, apple_dict):
        return cls(
            adam_id=apple_dict.get("adamId"),
            app_name=apple_dict.get("appName"),
            country_or_region_codes=apple_dict.get("countryOrRegionCodes"),
            developer_name=apple_dict.get("developerName")
        )

    def to_apple_dict(self):
        return {
            "adamId": self.adam_id,
            "appName": self.app_name,
            "countryOrRegionCodes": self.country_or_region_codes,
            "developerName": self.developer_name
        }
