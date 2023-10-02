# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : creative_model
# Time       ：2023/9/4 17:17
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from dataclasses import dataclass
from typing import List


@dataclass
class CreativesModel:
    adam_id: int
    creation_time: str
    creative_id: int
    modification_time: str
    name: str
    org_id: int
    state: str
    state_reasons: List
    creative_type: str

    @classmethod
    def from_apple_dict(cls, apple_dict):
        return cls(
            adam_id=apple_dict.get("adamId"),
            creation_time=apple_dict.get("creationTime"),
            creative_id=apple_dict.get("id"),
            modification_time=apple_dict.get("modificationTime"),
            name=apple_dict.get("name"),
            org_id=apple_dict.get("orgId"),
            state=apple_dict.get("state"),
            state_reasons=apple_dict.get("stateReasons"),
            creative_type=apple_dict.get("type"),
        )

    def to_apple_dict(self):
        return {
            "adamId": self.adam_id,
            "creationTime": self.creation_time,
            "id": self.creative_id,
            "modificationTime": self.modification_time,
            "name": self.name,
            "org_id": self.org_id,
            "state": self.state,
            "stateReasons": self.state_reasons,
            "type": self.creative_type,
        }
