# -*- coding: utf-8 -*-
# File generated from our OpenAPI spec
from __future__ import absolute_import, division, print_function

from stripe.api_resources.abstract import SingletonAPIResource
from stripe.stripe_object import StripeObject
from typing import Any, Optional
from typing_extensions import Literal


class FinancingSummary(SingletonAPIResource["FinancingSummary"]):
    """
    A financing object describes an account's current financing state. Used by Connect
    platforms to read the state of Capital offered to their connected accounts.
    """

    OBJECT_NAME = "capital.financing_summary"
    details: Optional[StripeObject]
    financing_offer: Optional[str]
    object: Literal["capital.financing_summary"]
    status: Optional[Literal["accepted", "delivered", "none"]]

    @classmethod
    def retrieve(cls, **params: Any) -> "FinancingSummary":
        instance = cls(None, **params)
        instance.refresh()
        return instance

    @classmethod
    def class_url(cls):
        return "/v1/capital/financing_summary"
