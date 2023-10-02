# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : campaign
# Time       ：2023/7/26 17:26
# Author     ：leo.wang
# version    ：python 3.9
# Description：
"""
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class CampaignModel:
    campaign_id: int
    adam_id: int
    ad_channel_type: str
    billing_event: str
    budget_amount: Dict
    budget_orders: List
    countries_or_regions: List
    country_or_region_serving_state_reasons: Dict
    creation_time: str
    daily_budget_amount: Dict
    deleted: bool
    display_status: str
    loc_invoice_details: Dict
    modification_time: str
    name: str
    org_id: int
    payment_model: str
    serving_state_reasons: List
    serving_status: str
    start_time: str
    end_time: str
    status: str
    supply_sources: List

    @classmethod
    def from_apple_dict(cls, apple_dict):
        return cls(
            org_id=apple_dict.get('orgId'),
            adam_id=apple_dict.get('adamId'),
            name=apple_dict.get('name'),
            countries_or_regions=apple_dict.get('countriesOrRegions'),
            ad_channel_type=apple_dict.get('adChannelType'),
            billing_event=apple_dict.get("billingEvent"),
            budget_amount=apple_dict.get('budgetAmount'),
            daily_budget_amount=apple_dict.get("dailyBudgetAmount"),
            status=apple_dict.get('status'),
            supply_sources=apple_dict.get('supplySources'),
            campaign_id=apple_dict.get('id'),
            start_time=apple_dict.get("startTime"),
            end_time=apple_dict.get("endTime"),
            budget_orders=apple_dict.get('budgetOrders'),
            country_or_region_serving_state_reasons=apple_dict.get("countryOrRegionServingStateReasons"),
            creation_time=apple_dict.get("creationTime"),
            deleted=apple_dict.get("deleted"),
            display_status=apple_dict.get("displayStatus"),
            loc_invoice_details=apple_dict.get("locInvoiceDetails"),
            modification_time=apple_dict.get('modificationTime'),
            payment_model=apple_dict.get('paymentModel'),
            serving_state_reasons=apple_dict.get('servingStateReasons'),
            serving_status=apple_dict.get('servingStatus')
        )

    def to_apple_dict(self):
        return {
            'id': self.campaign_id,
            'adamId': self.adam_id,
            'name': self.name,
            'countriesOrRegions': self.countries_or_regions,
            'adChannelType': self.ad_channel_type,
            'billingEvent': self.billing_event,
            'budgetAmount': self.budget_amount,
            'dailyBudgetAmount': self.daily_budget_amount,
            'status': self.status,
            'supplySources': self.supply_sources,
            'startTime': self.start_time,
            'endTime': self.end_time,
            'budgetOrders': self.budget_orders,
            'countryOrRegionServingStateReasons': self.country_or_region_serving_state_reasons,
            'creationTime': self.creation_time,
            'deleted': self.deleted,
            'displayStatus': self.display_status,
            'locInvoiceDetails': self.loc_invoice_details,
            'modificationTime': self.modification_time,
            'paymentModel': self.payment_model,
            'servingStateReasons': self.serving_state_reasons,
            'servingStatus': self.serving_status,
        }
