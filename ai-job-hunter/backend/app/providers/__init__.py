"""Pluggable live-job provider adapters."""

from app.providers.registry import build_provider_registry

__all__ = ["build_provider_registry"]
