"""Test the models and their validations."""

from darbia.shipping.types import Address

def test_address_models() -> None:
    """Test the address models."""
    assert Address() == Address()
