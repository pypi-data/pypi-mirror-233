# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : custom_report_response
# Time       ：2023/9/4 17:58
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class CustomReportResponseModel:
    creation_time: str
    dimensions: List
    download_uri: str
    end_time: str
    granularity: str
    report_id: int
    metrics: List
    modification_time: str
    name: str
    selector: Dict
    start_time: str
    state: str


@classmethod
def from_apple_dict(cls, apple_dict):
    return cls(
        creation_time=apple_dict.get("creationTime"),
        dimensions=apple_dict.get("dimensions"),
        download_uri=apple_dict.get("downloadUri"),
        end_time=apple_dict.get("endTime"),
        granularity=apple_dict.get("granularity"),
        report_id=apple_dict.get("id"),
        metrics=apple_dict.get("metrics"),
        modification_time=apple_dict.get("modificationTime"),
        name=apple_dict.get("name"),
        selector=apple_dict.get("selector"),
        start_time=apple_dict.get("startTime"),
        state=apple_dict.get("state")
    )


def to_apple_dict(self):
    return {
        "creationTime": self.creation_time,
        "dimensions": self.dimensions,
        "downloadUri": self.download_uri,
        "endTime": self.end_time,
        "granularity": self.granularity,
        "id": self.report_id,
        "metrics": self.metrics,
        "modificationTime": self.modification_time,
        "name": self.name,
        "selector": self.selector,
        "startTime": self.start_time,
        "state": self.state
    }
