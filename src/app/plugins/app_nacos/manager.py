import requests
from config import NACOS_SERVER
import random
from app.utils.log_util import logger


async def register_service(service_name, host, port):
    url = f"http://{NACOS_SERVER}/nacos/v2/ns/instance"
    data = {"serviceName": service_name, "ip": host, "port": port}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.post(url=url, data=data, headers=headers)
        if response.status_code == 200:
            logger.info(
                f"Service {service_name} with host {host} and port {port} registered successfully"
            )
        else:
            logger.error(f"response: {response.text}")
            logger.error(
                f"Failed to register service {service_name} with host {host} and port {port}"
            )
    except requests.RequestException as e:
        logger.error(f"Failed to connect to service: {e}")


def get_service_instance(service_name):
    url = f"http://{NACOS_SERVER}/nacos/v1/ns/instance/list?serviceName={service_name}"
    try:
        response = requests.get(url)
        instances = response.json().get("hosts", [])
        if not instances:
            logger.error(f"No instances available for service: {service_name}")
            return None
        instance = random.choice(instances)
        return instance.get("ip") + ":" + str(instance.get("port"))
    except requests.RequestException as e:
        logger.error(f"Failed to connect to service: {e}")
        return None


async def send_heartbeat(service_name, host, port):
    url = f"http://{NACOS_SERVER}/nacos/v1/ns/instance/beat?serviceName={service_name}&ip={host}&port={port}"
    response = requests.put(url)
    if response.status_code == 200:
        logger.info("Heartbeat sent successfully")
    else:
        logger.error("Failed to send heartbeat")
