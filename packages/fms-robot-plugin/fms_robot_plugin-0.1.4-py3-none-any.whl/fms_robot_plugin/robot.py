from typing import Callable, Optional

import time
import datetime
import logging

from fms_robot_plugin.typings import LaserScan, Twist, Pose, Map, MapResult
from fms_robot_plugin.mqtt import MqttClient, MqttConsumer


class Robot:
    robot_key: Optional[str]

    def __init__(
        self,
        robot_key: str,
        broker_host: str = "broker.movelrobotics.com",
        broker_port: int = 1883,
        heartbeat_interval_secs: int = 1,
        debug: bool = False,
    ):
        self.robot_key = robot_key

        self.broker_host = broker_host
        self.broker_port = broker_port
        self.mqtt = MqttClient(broker_host, broker_port)

        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    def run(self):
        self.maintain_connection()

    """
    Command Callbacks

    These methods are called when a command is published from the FMS server.
    """

    def on_teleop(self, cb: Callable[[Twist], None]):
        topic = f"robots/{self.robot_key}/teleop"
        self.consumer(topic).consume(lambda data: cb(Twist(**data)))

    def on_start_mapping(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/mapping/start"
        self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_stop_mapping(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/mapping/stop"
        self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_save_mapping(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/mapping/save"
        self.consumer(topic).consume(lambda _: cb(), serialize=False)

    """
    Publishers

    These methods are called to publish data to the FMS server.
    """

    def set_heartbeat(self):
        self.mqtt.publish(f"robots/{self.robot_key}/heartbeat", {"sent_at": datetime.datetime.utcnow().isoformat()})

    def set_camera_feed(self, data: str):
        self.mqtt.publish(f"robots/{self.robot_key}/camera", data, serialize=False)

    def set_lidar(self, data: LaserScan):
        self.mqtt.publish(f"robots/{self.robot_key}/lidar", data.dict())

    def set_pose(self, data: Pose):
        self.mqtt.publish(f"robots/{self.robot_key}/pose", data.dict())

    def set_map_data(self, data: Map):
        self.mqtt.publish(f"robots/{self.robot_key}/mapping/data", data.dict())

    def set_map_result(self, data: MapResult):
        self.mqtt.publish(f"robots/{self.robot_key}/mapping/result", data.dict())

    """
    Utilities
    """

    def consumer(self, topic: str):
        return MqttConsumer(topic, self.broker_host, self.broker_port)

    def maintain_connection(self):
        while True:
            self.set_heartbeat()
            time.sleep(1)
