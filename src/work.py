import asyncio
from src.socket_service import SocketService
from src.models.requests import WorkUnit
from dummy_response import audit


# TODO: If the UI never connects persist the result for sometime
# and return it when the UI tries to connect


# TODO: Bring back ast building in the worker
async def process_work(work: WorkUnit):

    steps = 5
    for i in range(steps):
        await asyncio.sleep(0.5)
        await SocketService.send(
            {"status": "analyzing", "progress": {"current": i + 1, "total": steps}}
        )

    await SocketService.send({"status": "complete", "done": True, "result": audit})
    await SocketService.close()
