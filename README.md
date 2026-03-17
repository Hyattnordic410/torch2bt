# torch2bt

**The bridge between PyTorch research and the Bittensor decentralized intelligence network.**

Turn any `torch.nn.Module` into a revenue-generating Bittensor miner — zero boilerplate.

## How it works

1. **Inspect** — Analyzes your model's `forward()` signature via reflection
2. **Synthesize** — Generates `protocol.py`, `miner.py`, and `Dockerfile` using Python 3.14 t-strings
3. **Deploy** — Drop the output into any GPU host and start mining

## Install

```bash
uv add torch2bt
```

## Usage

```python
import torch2bt as t2b
from my_models import SuperNeuralNet

t2b.package(
    model=SuperNeuralNet(),
    target_subnet=18,
    optimization="fp16",
    wallet_name="mining_key",
)
```

Output: `torch2bt_output/protocol.py`, `miner.py`, `Dockerfile`, `pyproject.toml`

## Supported subnets

| NetUID | Name            | Optimizations     |
|--------|-----------------|-------------------|
| 1      | Text Prompting  | FP32/FP16/BF16/INT8/INT4 |
| 18     | Cortex          | FP16/BF16         |

## Local testing

```python
from torch2bt.testing import MockValidator

validator = MockValidator(MySynapse, subnet_id=18, forward_fn=my_forward)
result = validator.query({"prompt": "a red cat"})
```

## Examples

### SN1 — Text Prompting

```python
import torch
import torch.nn as nn
import torch2bt as t2b
from torch2bt.testing import MockValidator, MockSynapse

class TinyLM(nn.Module):
    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        ...

t2b.package(TinyLM(), target_subnet=1, optimization="fp16", wallet_name="my_wallet")

# Local test — no live network needed
async def my_forward(synapse: MockSynapse) -> MockSynapse:
    synapse.completion = "Paris"
    return synapse

validator = MockValidator("Prompting", subnet_id=1, forward_fn=my_forward)
result = await validator.query({"roles": ["user"], "messages": ["Capital of France?"]})
print(result.completion)  # Paris
```

### SN18 — Image Generation (Cortex)

```python
import torch
import torch.nn as nn
import torch2bt as t2b
from torch2bt.testing import MockValidator, MockSynapse

class TinyDiffusion(nn.Module):
    def forward(self, noise: torch.Tensor) -> torch.Tensor:
        ...

# SN18 only supports fp16 / bf16
t2b.package(TinyDiffusion(), target_subnet=18, optimization="fp16", wallet_name="my_wallet")

async def my_forward(synapse: MockSynapse) -> MockSynapse:
    synapse.image_data = [0.0] * (64 * 64 * 3)
    synapse.image_shape = (64, 64, 3)
    return synapse

validator = MockValidator("ImageResponse", subnet_id=18, forward_fn=my_forward)
result = await validator.query({"prompt": "a red cat", "seed": 42, "width": 64, "height": 64, "num_inference_steps": 20})
print(result.image_shape)  # (64, 64, 3)
```

> Full runnable scripts in [`examples/`](examples/).

## Roadmap

- **Alpha** — `package()` for SN1 + SN18, mock validator
- **Beta** — RunPod/Lambda deploy API, auto-quantization
- **Production** — Multi-subnet mining, self-healing miners
