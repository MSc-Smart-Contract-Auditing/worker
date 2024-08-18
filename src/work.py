import asyncio
from src.socket_service import SocketService
from src.models.requests import WorkUnit
from dummy_response import audit

from src.smart_contracts.dependency_tree import DependencyTree

from src.analysis.model import MODEL


def get_dependency_tree(data: WorkUnit):
    return DependencyTree(data)


# TODO: If the UI never connects persist the result for sometime
# and return it when the UI tries to connect
async def process_work(work: WorkUnit):
    await SocketService.send({"status": "building_dt"})

    dt = get_dependency_tree(work)

    dt = DependencyTree(work)

    for item in dt.lookup.items():
        print(item)

    print()
    print()

    ids = dt.get_main_ids()

    result = dt.tree(ids[0])

    print(result["main"])
    for dependency in result["dependencies"]:
        print(dependency)

    steps = 5
    for i in range(steps):
        await asyncio.sleep(0.5)
        await SocketService.send(
            {"status": "analyzing", "progress": {"current": i + 1, "total": steps}}
        )

    await SocketService.send({"status": "complete", "done": True, "result": audit})
    await SocketService.close()
