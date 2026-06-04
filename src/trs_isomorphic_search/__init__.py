"""
TRS Alliance Structural Truth Layer.

Graph Isomorphism Validation for high-trust reference architectures.
"""

__version__ = "0.1.0"

from .models import SystemGraph, ValidationReport
from .validator import validate_isomorphism

__all__ = ["SystemGraph", "ValidationReport", "validate_isomorphism"]
