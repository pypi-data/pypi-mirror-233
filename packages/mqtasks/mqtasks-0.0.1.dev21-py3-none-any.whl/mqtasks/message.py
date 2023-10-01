from asyncio import AbstractEventLoop
from logging import Logger

from mqtasks.body import MqTaskBody


class MqTaskMessage:
    loop: AbstractEventLoop
    logger: Logger

    message_id: str
    name: str
    id: str
    body: MqTaskBody

    def __init__(
            self,
            logger: Logger,
            loop: AbstractEventLoop,
            message_id: str,
            task_name: str,
            task_id: str,
            task_body: MqTaskBody
    ):
        self.logger = logger
        self.loop = loop
        self.message_id = message_id
        self.name = task_name
        self.id = task_id
        self.body = task_body

    def __str__(self):
        return f"({MqTaskMessage.__name__} task_id:{self.id} task_name:{self.name} message_id:{self.message_id} body:{self.body.body})"
