from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Frequency(Enum):
    """How often a Task recurs."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Task:
    description: str
    time: str  # "HH:MM" 24-hour format, e.g. "07:00"
    frequency: Frequency
    completed: bool = False

    def markCompleted(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    age: int
    # Pet is the single store for its own tasks.
    taskList: List[Task] = field(default_factory=list)


@dataclass
class Owner:
    name: str
    petList: List[Pet] = field(default_factory=list)

    def addPet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        if pet not in self.petList:
            self.petList.append(pet)

    def removePet(self, pet: Pet) -> None:
        """Remove a pet from this owner's pet list."""
        if pet in self.petList:
            self.petList.remove(pet)

    def getTasks(self) -> List[Task]:
        """Return all tasks across every pet owned by this owner."""
        # Aggregate every pet's tasks; pets own them, Owner just exposes them.
        return [task for pet in self.petList for task in pet.taskList]


@dataclass
class Scheduler:
    # Stateless query/organize layer over the owner's pets. Tasks live on Pets,
    # so there is no separate `schedule` store to drift out of sync.
    owner: Owner

    def scheduleTask(self, pet: Pet, task: Task) -> None:
        """Add a task to the given pet's task list."""
        if task not in pet.taskList:
            pet.taskList.append(task)

    def removeTask(self, pet: Pet, task: Task) -> None:
        """Remove a task from the given pet's task list."""
        if task in pet.taskList:
            pet.taskList.remove(task)

    def getTasksByPet(self, pet: Pet) -> List[Task]:
        """Return the given pet's task list."""
        return list(pet.taskList)

    def getAllTasks(self) -> List[Task]:
        """Return all tasks across every pet for the owner."""
        # Delegate to Owner rather than re-walking petList here.
        return self.owner.getTasks()

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted chronologically by their "HH:MM" time string."""
        tasks = self.getAllTasks() if tasks is None else tasks
        return sorted(tasks, key=lambda t: tuple(int(part) for part in t.time.split(":")))

    def filter_by_pet(self, pet: Pet, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return only the tasks belonging to the given pet, from tasks (default: all tasks)."""
        tasks = self.getAllTasks() if tasks is None else tasks
        return [t for t in tasks if t in pet.taskList]

    def filter_by_status(self, completed: bool, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return only tasks whose completed flag matches, from tasks (default: all tasks)."""
        tasks = self.getAllTasks() if tasks is None else tasks
        return [t for t in tasks if t.completed == completed]
