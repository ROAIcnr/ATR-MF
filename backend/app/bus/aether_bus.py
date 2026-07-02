import asyncio
from typing import AsyncIterator
from .envelopes import AkashicEnvelope

class AetherBus:
    def __init__(self, maxsize: int = 10000):
        self._queue: asyncio.Queue[AkashicEnvelope] = asyncio.Queue(maxsize=maxsize)

    async def publish(self, envelope: AkashicEnvelope) -> None:
        await self._queue.put(envelope)

    async def subscribe(self) -> AsyncIterator[AkashicEnvelope]:
        while True:
            envelope = await self._queue.get()
            yield envelope
            self._queue.task_done()

aether_bus = AetherBus()
