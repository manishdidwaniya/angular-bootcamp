"""Provider registry."""

import httpx

from app.providers.adzuna import AdzunaProvider
from app.providers.arbeitnow import ArbeitnowProvider
from app.providers.base import JobProvider
from app.providers.themuse import TheMuseProvider
from app.providers.weworkremotely import WeWorkRemotelyProvider


def build_provider_registry(client: httpx.AsyncClient) -> list[JobProvider]:
    return [
        ArbeitnowProvider(client),
        WeWorkRemotelyProvider(client),
        TheMuseProvider(client),
        AdzunaProvider(client),
    ]
