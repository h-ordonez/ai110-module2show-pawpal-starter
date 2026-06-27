from dataclasses import dataclass, field
from datetime import date
from typing import List, Dict, Optional


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
    pet: Pet

    def isDone(self) -> bool:
        pass


@dataclass
class Owner:
    name: str
    petList: List[Pet] = field(default_factory=list)
    # Back-reference to the Scheduler, which is the source of truth for tasks.
    # Set when the Owner is attached to a Scheduler; getTasks() delegates to it.
    scheduler: Optional["Scheduler"] = None

    def addPet(self, pet: Pet) -> None:
        pass

    def removePet(self, pet: Pet) -> None:
        pass

    def getTasks(self) -> List[Task]:
        # Delegates to the Scheduler rather than holding its own task list.
        pass


@dataclass
class Scheduler:
    owner: Owner
    schedule: Dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Complete the bidirectional link so Owner.getTasks() can delegate here.
        self.owner.scheduler = self

    def scheduleTask(self, task: Task, date: date) -> None:
        pass

    def removeTask(self, task: Task) -> None:
        pass

    def getUpcomingTasks(self) -> List[Task]:
        pass

    def getTasksByPet(self, pet: Pet) -> List[Task]:
        pass
