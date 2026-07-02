from datetime import time

from pawpal_system import Frequency, Owner, Pet, Scheduler, Task


def test_mark_completed_sets_task_as_done():
    task = Task("Morning walk", time(7, 0), Frequency.DAILY)
    assert task.completed is False

    task.markCompleted()

    assert task.completed is True


def test_scheduling_task_increases_pet_task_count():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    assert len(pet.taskList) == 0

    scheduler.scheduleTask(pet, Task("Morning walk", time(7, 0), Frequency.DAILY))

    assert len(pet.taskList) == 1
