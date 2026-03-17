"""Subnet 18 (SN18) — Cortex image generation protocol adapter."""

from __future__ import annotations

from torch2bt.models import Optimization, SubnetProtocol
from torch2bt.subnets.base import BaseSubnet


class Subnet18(BaseSubnet):
    """SN18: Cortex — text-to-image generation via the ImageResponse synapse."""

    @property
    def protocol(self) -> SubnetProtocol:
        """Return the SN18 Cortex protocol specification."""
        return SubnetProtocol(
            subnet_id=18,
            name="Cortex",
            synapse_class="ImageResponse",
            description="Text-to-image generation synapse for Bittensor SN18 Cortex.",
            input_spec={
                "prompt": "str",
                "seed": "int",
                "width": "int",
                "height": "int",
                "num_inference_steps": "int",
            },
            output_spec={
                "image_data": "list[float] | None",
                "image_shape": "tuple[int, int, int] | None",
            },
            compatible_optimizations=[
                Optimization.FP16,
                Optimization.BF16,
            ],
        )
