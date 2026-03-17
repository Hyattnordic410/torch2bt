"""Example: Package an image generation model for Bittensor SN18 (Cortex).

SN18 expects a model that takes a prompt + seed + dimensions and returns
image_data (flat float list) + image_shape (H, W, C).
Only FP16/BF16 optimizations are supported on SN18.
"""

from __future__ import annotations

import asyncio

import torch
import torch.nn as nn

import torch2bt as t2b
from torch2bt.testing import MockSynapse, MockValidator


class TinyDiffusion(nn.Module):
    """Minimal image generation stub for SN18 demonstration."""

    def __init__(self, latent_dim: int = 128) -> None:
        """Initialize model weights."""
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 64 * 64 * 3),
            nn.Sigmoid(),
        )

    def forward(self, noise: torch.Tensor) -> torch.Tensor:
        """Generate an image from a noise vector.

        Args:
            noise: Latent noise tensor of shape (batch, latent_dim).

        Returns:
            Flat pixel tensor of shape (batch, H*W*C).
        """
        return self.net(noise)


# ---------------------------------------------------------------------------
# 1. Package the model — SN18 only supports fp16 / bf16
# ---------------------------------------------------------------------------
model = TinyDiffusion()
result = t2b.package(
    model=model,
    target_subnet=18,
    optimization="fp16",
    wallet_name="my_miner_wallet",
    output_dir="./output/sn18_miner",
)

print("Generated files:")
for name, path in result.__dict__.items():
    if hasattr(path, "exists"):
        print(f"  {name}: {path}")


# ---------------------------------------------------------------------------
# 2. Local test with MockValidator
# ---------------------------------------------------------------------------
async def my_forward(synapse: MockSynapse) -> MockSynapse:
    """Stub forward that returns a tiny 64x64 RGB image filled with zeros."""
    h, w, c = 64, 64, 3
    synapse.image_data = [0.0] * (h * w * c)
    synapse.image_shape = (h, w, c)
    return synapse


async def main() -> None:
    """Run a quick local validation."""
    validator = MockValidator(
        synapse_class="ImageResponse",
        subnet_id=18,
        forward_fn=my_forward,
    )

    result = await validator.query(
        {
            "prompt": "a red cat sitting on a bench",
            "seed": 42,
            "width": 64,
            "height": 64,
            "num_inference_steps": 20,
        }
    )

    print("\nMock query result:")
    print(f"  image_shape: {result.image_shape}")
    print(f"  image_data length: {len(result.image_data)}")
    print(f"  total queries: {validator.query_count}")

    # Run a test suite with multiple prompts
    suite_results = await validator.run_test_suite(
        [
            {
                "prompt": "a sunset over mountains",
                "seed": 1,
                "width": 64,
                "height": 64,
                "num_inference_steps": 20,
            },
            {
                "prompt": "a futuristic city",
                "seed": 2,
                "width": 64,
                "height": 64,
                "num_inference_steps": 20,
            },
        ]
    )
    print(f"  test suite passed: {len(suite_results)}/2")


asyncio.run(main())
