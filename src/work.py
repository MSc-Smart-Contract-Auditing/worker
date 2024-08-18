import asyncio
from src.socket_service import SocketService
from src.models.requests import WorkUnit
from dummy_response import audit

from src.smart_contracts.dependency_tree import DependencyTree

from src.analysis.model import MODEL


# TODO: If the UI never connects persist the result for sometime
# and return it when the UI tries to connect
async def process_work(work: WorkUnit):
    await asyncio.sleep(0.5)
    await SocketService.send({"status": "building_dt"})
    dt = DependencyTree(work)
    main_ids = dt.get_main_ids()

    vulnerabilities = []

    for idx, id in enumerate(main_ids):
        await SocketService.send(
            {
                "status": "analyzing",
                "progress": {"current": idx + 1, "total": len(main_ids)},
            }
        )
        codeblocks = dt.tree(id)
        input = codeblocks["main"] + "\n\n" + "\n\n".join(codeblocks["dependencies"])
        output = MODEL.analyze(input)

        if output.startswith("There is no vulnerability"):
            continue

        vulnerabilities.append(output)

    # await SocketService.send({"status": "finishing"})

    if len(vulnerabilities) == 0:
        result = """There are no detected vulnerabilities in the provided contract!

However, this model can make mistakes. Do not resort to this tool as a sole measure of security."""
    elif len(vulnerabilities) == 1:
        result = vulnerabilities[0]
    else:
        result = MODEL.merge(vulnerabilities)

    await SocketService.send({"status": "complete", "done": True, "result": result})
    await SocketService.close()
