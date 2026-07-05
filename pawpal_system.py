import calendar
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum
from typing import List, Optional, Tuple


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
    dueDate: date = field(default_factory=date.today)

    def markCompleted(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_due_date(self) -> date:
        """Return the date this task's next occurrence falls on, based on frequency."""
        if self.frequency == Frequency.DAILY:
            return self.dueDate + timedelta(days=1)
        if self.frequency == Frequency.WEEKLY:
            return self.dueDate + timedelta(days=7)
        if self.frequency == Frequency.MONTHLY:
            month = self.dueDate.month % 12 + 1
            year = self.dueDate.year + (self.dueDate.month // 12)
            day = min(self.dueDate.day, calendar.monthrange(year, month)[1])
            return self.dueDate.replace(year=year, month=month, day=day)
        raise ValueError(f"Unknown frequency: {self.frequency}")


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

    def complete_task(self, pet: Pet, task: Task) -> Task:
        """Mark a task done and automatically schedule its next occurrence for the same pet."""
        task.markCompleted()
        next_task = Task(
            description=task.description,
            time=task.time,
            frequency=task.frequency,
            dueDate=task.next_due_date(),
        )
        self.scheduleTask(pet, next_task)
        return next_task

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

    def _pending_slots(self):
        """Group each pet's still-pending tasks by (dueDate, time) slot."""
        slots = {}
        for pet in self.owner.petList:
            for task in pet.taskList:
                if not task.completed:
                    slots.setdefault((task.dueDate, task.time), []).append((pet, task))
        return slots

    def find_same_pet_conflicts(self) -> List[Tuple[Pet, Task, Task]]:
        """Return (pet, task1, task2) triples where one pet has 2+ pending tasks in the same slot."""
        conflicts = []
        for slot in self._pending_slots().values():
            for i in range(len(slot)):
                for j in range(i + 1, len(slot)):
                    pet_i, task_i = slot[i]
                    pet_j, task_j = slot[j]
                    if pet_i is pet_j:
                        conflicts.append((pet_i, task_i, task_j))
        return conflicts

    def find_cross_pet_conflicts(self) -> List[Tuple[Pet, Task, Pet, Task]]:
        """Return (pet1, task1, pet2, task2) quadruples where two different pets share a slot."""
        conflicts = []
        for slot in self._pending_slots().values():
            for i in range(len(slot)):
                for j in range(i + 1, len(slot)):
                    pet_i, task_i = slot[i]
                    pet_j, task_j = slot[j]
                    if pet_i is not pet_j:
                        conflicts.append((pet_i, task_i, pet_j, task_j))
        return conflicts

    def get_conflict_warnings(self) -> List[str]:
        """Return a human-readable warning message for every detected scheduling conflict."""
        warnings = []
        for pet, task1, task2 in self.find_same_pet_conflicts():
            warnings.append(
                f"Conflict: {pet.name} has '{task1.description}' and '{task2.description}' "
                f"both scheduled at {task1.time} on {task1.dueDate}."
            )
        for pet1, task1, pet2, task2 in self.find_cross_pet_conflicts():
            warnings.append(
                f"Conflict: {pet1.name}'s '{task1.description}' and {pet2.name}'s "
                f"'{task2.description}' are both scheduled at {task1.time} on {task1.dueDate}."
            )
        return warnings
