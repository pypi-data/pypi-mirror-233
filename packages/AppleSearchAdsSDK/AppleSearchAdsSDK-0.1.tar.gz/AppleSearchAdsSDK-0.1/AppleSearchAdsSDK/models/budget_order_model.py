# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : budget_order_model
# Time       ：2023/9/4 16:43
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class BudgetOrderModel:
    billing_email: str
    budget: Dict
    client_name: str
    end_date: str
    budget_order_id: int
    name: str
    order_number: str
    parent_org_id: int
    primary_buyer_email: str
    primary_buyer_name: str
    start_date: str
    status: str
    supply_sources: List

    @classmethod
    def from_apple_dict(cls, apple_dict):
        return cls(
            billing_email=apple_dict.get("billingEmail"),
            budget=apple_dict.get("budget"),
            client_name=apple_dict.get("clientName"),
            end_date=apple_dict.get("endDate"),
            budget_order_id=apple_dict.get("id"),
            name=apple_dict.get("name"),
            order_number=apple_dict.get("orderNumber"),
            parent_org_id=apple_dict.get("parentOrgId"),
            primary_buyer_email=apple_dict.get("primaryBuyerEmail"),
            primary_buyer_name=apple_dict.get("primaryBuyerName"),
            start_date=apple_dict.get("startDate"),
            status=apple_dict.get("status"),
            supply_sources=apple_dict.get("supplySources")
        )

    def to_apple_dict(self):
        return {
            "billingEmail": self.billing_email,
            "budget": self.budget,
            "clientName": self.client_name,
            "endDate": self.end_date,
            "id": self.budget_order_id,
            "name": self.name,
            "orderNumber": self.order_number,
            "parentOrgId": self.parent_org_id,
            "primaryBuyerEmail": self.primary_buyer_email,
            "primaryBuyerName": self.primary_buyer_name,
            "startDate": self.start_date,
            "status": self.status,
            "supplySources": self.supply_sources,
        }
