# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : product_page_detail_model
# Time       ：2023/9/4 17:32
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from dataclasses import dataclass


@dataclass
class ProductPageDetailModel:
    adam_id: int
    creation_time: str
    product_page_detail_id: str
    modification_time: str
    name: str
    state: str

    @classmethod
    def from_apple_dict(cls, apple_dict):
        return cls(
            adam_id=apple_dict.get("adamId"),
            creation_time=apple_dict.get("creationTime"),
            product_page_detail_id=apple_dict.get("id"),
            modification_time=apple_dict.get("modificationTime"),
            name=apple_dict.get("name"),
            state=apple_dict.get("state")
        )

    def to_apple_dict(self):
        return {
            "adamId": self.adam_id,
            "creationTime": self.creation_time,
            "id": self.product_page_detail_id,
            "modificationTime": self.modification_time,
            "name": self.name,
            "state": self.state,
        }
