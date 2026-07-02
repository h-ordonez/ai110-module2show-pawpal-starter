from datetime import time

from pawpal_system import Frequency, Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Sam")

    rex = Pet("Rex", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 5)

    owner.addPet(rex)
    owner.addPet(whiskers)

    scheduler = Scheduler(owner)

    scheduler.scheduleTask(rex, Task("Morning walk", time(7, 0), Frequency.DAILY))
    scheduler.scheduleTask(rex, Task("Lunchtime feeding", time(12, 0), Frequency.DAILY))
    scheduler.scheduleTask(rex, Task("Evening walk", time(18, 30), Frequency.DAILY))

    scheduler.scheduleTask(whiskers, Task("Breakfast", time(8, 0), Frequency.DAILY))
    scheduler.scheduleTask(whiskers, Task("Litter box cleaning", time(13, 30), Frequency.DAILY))
    scheduler.scheduleTask(whiskers, Task("Vet checkup", time(16, 0), Frequency.MONTHLY))

    print("Today's Schedule")
    for pet in owner.petList:
        print(f"\n{pet.name} ({pet.species}):")
        for task in scheduler.getTasksByPet(pet):
            print(f"  {task.time.strftime('%I:%M %p')} - {task.description}")


if __name__ == "__main__":
    main()
