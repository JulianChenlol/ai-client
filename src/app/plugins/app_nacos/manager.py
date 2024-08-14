import requests
from config import NACOS_SERVER
import random
from app.utils.log_util import logger


def register_service(service_name, host, port):
    url = f"{NACOS_SERVER}/nacos/v2/ns/instance"
    data = {"serviceName": service_name, "ip": host, "port": port, "metadata": {"version": "1.0"}}
    response = requests.post(url, json=data)
    logger.info(response.json())
    return response.json()


def get_service_instance(service_name):
    url = f"{NACOS_SERVER}/nacos/v2/ns/instance/list?serviceName={service_name}"
    try:
        response = requests.get(url)
        instances = response.json().get("hosts", [])
        if not instances:
            logger.error(f"No instances available for service: {service_name}")
            return None
        instance = random.choice(instances)
        return instance.get("ip") + ":" + instance.get("port")
    except requests.RequestException as e:
        logger.error(f"Failed to connect to service: {e}")
        return None


async def send_heartbeat(service_name, host, port):
    url = (
        f"{NACOS_SERVER}/nacos/v1/ns/instance/beat?serviceName={service_name}&ip={host}&port={port}"
    )
    response = requests.put(url)
    if response.status_code == 200:
        logger.info("Heartbeat sent successfully")
    else:
        logger.error("Failed to send heartbeat")
