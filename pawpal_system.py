from dataclasses import dataclass, field
from datetime import date
from typing import List, Dict


@dataclass
class Pet:
    name: str
    species: str
    age: int

    def getNeeds(self) -> str:
        pass


@dataclass
class Task:
    title: str
    description: str
    completed: bool
    dueDate: date

    def isDone(self) -> bool:
        pass


@dataclass
class Owner:
    name: str
    petList: List[Pet] = field(default_factory=list)
    taskList: List[Task] = field(default_factory=list)

    def addPet(self, pet: Pet) -> None:
        pass

    def removePet(self, pet: Pet) -> None:
        pass

    def getTasks(self) -> List[Task]:
        pass


@dataclass
class Scheduler:
    owner: Owner
    schedule: Dict = field(default_factory=dict)

    def scheduleTask(self, task: Task, date: date) -> None:
        pass

    def removeTask(self, task: Task) -> None:
        pass

    def getUpcomingTasks(self) -> List[Task]:
        pass

    def getTasksByPet(self, pet: Pet) -> List[Task]:
        pass
