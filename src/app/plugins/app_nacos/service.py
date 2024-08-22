from app.model.llm_model.service import get_all, check_service_health
from app.model.llm_model.schemas import LlmModel
from app.database.core import SessionLocal
from .manager import send_heartbeat, register_service
import asyncio
from app.utils.log_util import logger

HEART_BEAT_INTERVAL = 10

START = True


async def heartbeat_task(model: LlmModel):
    is_health = check_service_health(model.server_ip, model.server_port)
    if is_health:
        logger.info(f"Service is healthy for {model.name}")
        await send_heartbeat(model.name, model.server_ip, model.server_port)
        logger.info(f"Heartbeat sent for {model.name}")
    else:
        logger.error(f"Service is unhealthy for {model.name}")


async def start_nacos_client():
    await register_services()
    asyncio.create_task(send_heartbeats())


async def register_services():
    db_session = SessionLocal()
    models = get_all(db_session=db_session)
    tasks = []
    for model in models:
        for model in models:
            task = asyncio.create_task(
                register_service(model.name, model.server_ip, model.server_port)
            )
            tasks.append(task)
        await asyncio.gather(*tasks)


async def send_heartbeats():
    db_session = SessionLocal()
    global START
    while START:
        models = get_all(db_session=db_session)
        tasks = []
        for model in models:
            task = asyncio.create_task(heartbeat_task(model))
            tasks.append(task)
        await asyncio.gather(*tasks)
        await asyncio.sleep(HEART_BEAT_INTERVAL)


async def stop_nacos_client():
    global START
    START = False
    logger.info("Stopping heartbeat task")
