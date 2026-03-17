"""Example: Package a text generation model for Bittensor SN1 (Text Prompting).

SN1 expects a model that takes roles + messages and returns a completion string.
This example uses a tiny transformer-based language model as a stand-in.
"""

from __future__ import annotations

import asyncio

import torch
import torch.nn as nn

import torch2bt as t2b
from torch2bt.testing import MockSynapse, MockValidator


class TinyLM(nn.Module):
    """Minimal language model stub for SN1 demonstration."""

    def __init__(self, vocab_size: int = 512, d_model: int = 64) -> None:
        """Initialize model weights."""
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        self.transformer = nn.TransformerEncoderLayer(d_model=d_model, nhead=4, batch_first=True)
        self.head = nn.Linear(d_model, vocab_size)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        """Run a forward pass.

        Args:
            input_ids: Token id tensor of shape (batch, seq_len).

        Returns:
            Logits of shape (batch, seq_len, vocab_size).
        """
        x = self.embed(input_ids)
        x = self.transformer(x)
        return self.head(x)


# ---------------------------------------------------------------------------
# 1. Package the model
# ---------------------------------------------------------------------------
model = TinyLM()
result = t2b.package(
    model=model,
    target_subnet=1,
    optimization="fp16",
    wallet_name="my_miner_wallet",
    output_dir="./output/sn1_miner",
)

print("Generated files:")
for name, path in result.__dict__.items():
    if hasattr(path, "exists"):
        print(f"  {name}: {path}")


# ---------------------------------------------------------------------------
# 2. Local test with MockValidator (no live Bittensor network needed)
# ---------------------------------------------------------------------------
async def my_forward(synapse: MockSynapse) -> MockSynapse:
    """Stub forward that echoes back a fixed completion."""
    synapse.completion = f"Response to: {synapse.messages}"
    return synapse


async def main() -> None:
    """Run a quick local validation."""
    validator = MockValidator(
        synapse_class="Prompting",
        subnet_id=1,
        forward_fn=my_forward,
    )

    result = await validator.query(
        {
            "roles": ["user"],
            "messages": ["What is the capital of France?"],
        }
    )

    print("\nMock query result:")
    print(f"  completion: {result.completion}")
    print(f"  total queries: {validator.query_count}")


asyncio.run(main())
