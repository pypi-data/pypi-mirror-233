"""Shipping models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BillToSelector(str, Enum):
    """An enum for the shipment billing types."""

    SHIPPER = "shipper"
    THIRD_PARTY = "third_party"


@dataclass
class Address:
    """A street address."""

    company: str | None = None
    attention_to: str | None = None
    address1: str | None = None
    address2: str | None = None
    address3: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None


@dataclass
class BillingInfo:
    """A wrapper for a set of billing information."""

    bill_to: BillToSelector
    billing_account: str | None = None
    billing_address: Address | None = None


@dataclass
class Package:
    """A package."""

    weight: float
    length: float
    width: float
    height: float
    reference1: str | None = None
    reference2: str | None = None
    reference3: str | None = None
    reference4: str | None = None
    reference5: str | None = None


@dataclass
class Shipment:
    """A complete shipment."""

    ship_from: Address
    ship_to: Address
    billing: BillingInfo
    packages: list[Package]
    reference1: str | None = None
    reference2: str | None = None
    reference3: str | None = None
    reference4: str | None = None
    reference5: str | None = None
