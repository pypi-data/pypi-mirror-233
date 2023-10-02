# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : app_asset_model
# Time       ：2023/9/4 15:54
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from dataclasses import dataclass


@dataclass
class AppAssetModel:
    adam_id: int
    app_preview_device: str
    asset_gen_id: str
    asset_type: str
    asset_url: str
    asset_video_url: str
    deleted: bool
    orientation: str
    source_height: int
    source_width: int

    @classmethod
    def from_apple_dict(cls, apple_dict):
        return cls(
            adam_id=apple_dict.get("adamId"),
            app_preview_device=apple_dict.get("appPreviewDevice"),
            asset_gen_id=apple_dict.get("assetGenId"),
            asset_type=apple_dict.get("assetType"),
            asset_url=apple_dict.get("assetURL"),
            asset_video_url=apple_dict.get("assetVideoUrl"),
            deleted=apple_dict.get("deleted"),
            orientation=apple_dict.get("orientation"),
            source_height=apple_dict.get("sourceHeight"),
            source_width=apple_dict.get("sourceWidth"),
        )

    def to_apple_dict(self):
        return {
            "adamId": self.adam_id,
            "appPreviewDevice": self.app_preview_device,
            "assetGenId": self.asset_gen_id,
            "assetType": self.asset_type,
            "assetURL": self.asset_url,
            "assetVideoUrl": self.asset_video_url,
            "deleted": self.deleted,
            "orientation": self.orientation,
            "sourceHeight": self.source_height,
            "sourceWidth": self.source_width,
        }
