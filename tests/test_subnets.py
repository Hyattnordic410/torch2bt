"""Tests for the subnet protocol registry."""

from __future__ import annotations

import pytest

from torch2bt.models import Optimization
from torch2bt.subnets import SUPPORTED_SUBNETS, get_subnet_protocol
from torch2bt.subnets.subnet1 import Subnet1
from torch2bt.subnets.subnet18 import Subnet18


def test_supported_subnets_contains_phase_a() -> None:
    assert 1 in SUPPORTED_SUBNETS
    assert 18 in SUPPORTED_SUBNETS


def test_get_subnet1_protocol() -> None:
    protocol = get_subnet_protocol(1)
    assert protocol.subnet_id == 1
    assert protocol.synapse_class == "Prompting"
    assert "roles" in protocol.input_spec
    assert "completion" in protocol.output_spec


def test_get_subnet18_protocol() -> None:
    protocol = get_subnet_protocol(18)
    assert protocol.subnet_id == 18
    assert protocol.synapse_class == "ImageResponse"
    assert "prompt" in protocol.input_spec
    assert "image_data" in protocol.output_spec


def test_unsupported_subnet_raises() -> None:
    with pytest.raises(ValueError, match="not supported"):
        get_subnet_protocol(42)


def test_subnet1_supports_all_optimizations() -> None:
    adapter = Subnet1()
    for opt in Optimization:
        assert adapter.supports_optimization(opt)


def test_subnet18_does_not_support_fp32() -> None:
    adapter = Subnet18()
    assert not adapter.supports_optimization(Optimization.FP32)
    assert adapter.supports_optimization(Optimization.FP16)
    assert adapter.supports_optimization(Optimization.BF16)
