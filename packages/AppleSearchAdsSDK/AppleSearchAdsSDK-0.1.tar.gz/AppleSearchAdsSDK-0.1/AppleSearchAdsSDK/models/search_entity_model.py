# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : search_entity_model
# Time       ：2023/9/4 19:20
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from dataclasses import dataclass


@dataclass
class SearchEntityModel:
    admin_area: str
    country_or_region: str
    display_name: str
    entity: str
    entity_id: str
    locality: str

    @classmethod
    def from_apple_dict(cls, apple_dict):
        return cls(
            admin_area=apple_dict.get("adminArea"),
            country_or_region=apple_dict.get("countryOrRegion"),
            display_name=apple_dict.get("displayName"),
            entity=apple_dict.get("entity"),
            entity_id=apple_dict.get("id"),
            locality=apple_dict.get("locality"),
        )

    def to_apple_dict(self):
        return {
            "adminArea": self.admin_area,
            "countryOrRegion": self.country_or_region,
            "displayName": self.display_name,
            "entity": self.entity,
            "id": self.entity_id,
            "locality": self.locality
        }
