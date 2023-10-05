from typing import Optional, List

from pydantic import BaseModel


class QueueTask(BaseModel):
    name: str
    capacity: int


class QueueInfo(BaseModel):
    capacity: int = 12
    busy: int = 0
    free: int = capacity

    usage: List[QueueTask] = [
        QueueTask(name='detection_on_premice_clustering', capacity=1),
        QueueTask(name='detection_saas', capacity=12),
        QueueTask(name='classification_saas', capacity=12),
    ]
    in_queue: Optional[List[QueueTask]]
