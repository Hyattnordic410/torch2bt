"""Abstract base class for Bittensor subnet protocol adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod

from torch2bt.models import Optimization, SubnetProtocol


class BaseSubnet(ABC):
    """Abstract adapter that exposes a subnet's protocol specification."""

    @property
    @abstractmethod
    def protocol(self) -> SubnetProtocol:
        """Return the SubnetProtocol specification for this subnet."""
        ...

    def supports_optimization(self, opt: Optimization) -> bool:
        """Check whether an optimization strategy is supported by this subnet.

        Args:
            opt: The optimization strategy to check.

        Returns:
            True if the subnet protocol is compatible with the given optimization.
        """
        return opt in self.protocol.compatible_optimizations
