"""Subnet 1 (SN1) — Text Prompting protocol adapter."""

from __future__ import annotations

from torch2bt.models import Optimization, SubnetProtocol
from torch2bt.subnets.base import BaseSubnet


class Subnet1(BaseSubnet):
    """SN1: Text Prompting — conversational completions via the Prompting synapse."""

    @property
    def protocol(self) -> SubnetProtocol:
        """Return the SN1 Prompting protocol specification."""
        return SubnetProtocol(
            subnet_id=1,
            name="Text Prompting",
            synapse_class="Prompting",
            description="Conversational text-completion synapse for Bittensor SN1.",
            input_spec={
                "roles": "list[str]",
                "messages": "list[str]",
            },
            output_spec={
                "completion": "str",
            },
            compatible_optimizations=[
                Optimization.FP32,
                Optimization.FP16,
                Optimization.BF16,
                Optimization.INT8,
                Optimization.INT4,
            ],
        )
