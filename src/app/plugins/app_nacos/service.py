from app.model.llm_model.service import get_all, check_service_health
from app.model.llm_model.schemas import LlmModel
from app.database.core import SessionLocal
from .manager import send_heartbeat
import asyncio
from app.utils.log_util import logger

HEART_BEAT_INTERVAL = 10

START = True


async def heartbeat_task(model: LlmModel):
    url = f"{model.server_ip}:{model.server_port}/health"
    is_health = check_service_health(url)
    if is_health:
        logger.info(f"Service is healthy for {model.name}")
        await send_heartbeat(model.name, model.server_ip, model.server_port)
        logger.info(f"Heartbeat sent for {model.name}")
    else:
        logger.error(f"Service is unhealthy for {model.name}")


async def start_heartbeats():
    asyncio.create_task(send_heartbeats())


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


async def stop_heartbeats():
    global START
    START = False
    logger.info("Stopping heartbeat task")
