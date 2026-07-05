from pawpal_system import Frequency, Owner, Pet, Scheduler, Task


def format_12h(hhmm: str) -> str:
    """Render a "HH:MM" 24-hour string as "HH:MM AM/PM" for display."""
    hour, minute = (int(part) for part in hhmm.split(":"))
    period = "AM" if hour < 12 else "PM"
    hour12 = hour % 12 or 12
    return f"{hour12:02d}:{minute:02d} {period}"


def print_tasks(tasks) -> None:
    for task in tasks:
        status = "done" if task.completed else "pending"
        print(f"  {format_12h(task.time)} - {task.description} ({status})")


def main() -> None:
    owner = Owner("Sam")

    rex = Pet("Rex", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 5)

    owner.addPet(rex)
    owner.addPet(whiskers)

    scheduler = Scheduler(owner)

    # Added out of time-order on purpose, to exercise filter_by_pet / filter_by_status
    # independent of any sorting.
    evening_walk = Task("Evening walk", "18:30", Frequency.DAILY)
    morning_walk = Task("Morning walk", "07:00", Frequency.DAILY)
    lunch_feeding = Task("Lunchtime feeding", "12:00", Frequency.DAILY)
    scheduler.scheduleTask(rex, evening_walk)
    scheduler.scheduleTask(rex, morning_walk)
    scheduler.scheduleTask(rex, lunch_feeding)
    morning_walk.markCompleted()

    vet_checkup = Task("Vet checkup", "16:00", Frequency.MONTHLY)
    breakfast = Task("Breakfast", "08:00", Frequency.DAILY)
    litter_cleaning = Task("Litter box cleaning", "13:30", Frequency.DAILY)
    scheduler.scheduleTask(whiskers, vet_checkup)
    scheduler.scheduleTask(whiskers, breakfast)
    scheduler.scheduleTask(whiskers, litter_cleaning)
    breakfast.markCompleted()
    litter_cleaning.markCompleted()

    print("Today's Schedule")
    for pet in owner.petList:
        print(f"\n{pet.name} ({pet.species}):")
        print_tasks(scheduler.getTasksByPet(pet))

    print("\nfilter_by_pet(rex):")
    print_tasks(scheduler.filter_by_pet(rex))

    print("\nfilter_by_pet(whiskers):")
    print_tasks(scheduler.filter_by_pet(whiskers))

    print("\nfilter_by_status(completed=True):")
    print_tasks(scheduler.filter_by_status(True))

    print("\nfilter_by_status(completed=False):")
    print_tasks(scheduler.filter_by_status(False))


if __name__ == "__main__":
    main()
