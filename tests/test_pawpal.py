from datetime import date

from pawpal_system import Frequency, Owner, Pet, Scheduler, Task


def test_mark_completed_sets_task_as_done():
    task = Task("Morning walk", "07:00", Frequency.DAILY)
    assert task.completed is False

    task.markCompleted()

    assert task.completed is True


def test_scheduling_task_increases_pet_task_count():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    assert len(pet.taskList) == 0

    scheduler.scheduleTask(pet, Task("Morning walk", "07:00", Frequency.DAILY))

    assert len(pet.taskList) == 1


def test_sort_by_time_orders_tasks_chronologically():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    scheduler.scheduleTask(pet, Task("Evening walk", "18:30", Frequency.DAILY))
    scheduler.scheduleTask(pet, Task("Breakfast", "08:00", Frequency.DAILY))
    scheduler.scheduleTask(pet, Task("Lunch", "12:00", Frequency.DAILY))

    ordered = scheduler.sort_by_time()

    assert [t.description for t in ordered] == ["Breakfast", "Lunch", "Evening walk"]


def test_sort_by_time_handles_non_zero_padded_hours():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    scheduler.scheduleTask(pet, Task("Late walk", "9:05", Frequency.DAILY))
    scheduler.scheduleTask(pet, Task("Early walk", "9:00", Frequency.DAILY))

    ordered = scheduler.sort_by_time()

    assert [t.description for t in ordered] == ["Early walk", "Late walk"]


def test_filter_by_pet_returns_only_that_pets_tasks():
    owner = Owner("Sam")
    rex = Pet("Rex", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 2)
    owner.addPet(rex)
    owner.addPet(whiskers)
    scheduler = Scheduler(owner)

    scheduler.scheduleTask(rex, Task("Morning walk", "07:00", Frequency.DAILY))
    scheduler.scheduleTask(whiskers, Task("Breakfast", "08:00", Frequency.DAILY))

    filtered = scheduler.filter_by_pet(rex)

    assert [t.description for t in filtered] == ["Morning walk"]


def test_filter_by_pet_with_no_tasks_returns_empty_list():
    owner = Owner("Sam")
    rex = Pet("Rex", "dog", 3)
    owner.addPet(rex)
    scheduler = Scheduler(owner)

    assert scheduler.filter_by_pet(rex) == []


def test_filter_by_status_returns_only_matching_completion():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    done_task = Task("Morning walk", "07:00", Frequency.DAILY)
    done_task.markCompleted()
    pending_task = Task("Evening walk", "18:00", Frequency.DAILY)
    scheduler.scheduleTask(pet, done_task)
    scheduler.scheduleTask(pet, pending_task)

    assert scheduler.filter_by_status(True) == [done_task]
    assert scheduler.filter_by_status(False) == [pending_task]


def test_filter_by_status_composes_with_filter_by_pet():
    owner = Owner("Sam")
    rex = Pet("Rex", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 2)
    owner.addPet(rex)
    owner.addPet(whiskers)
    scheduler = Scheduler(owner)

    rex_done = Task("Morning walk", "07:00", Frequency.DAILY)
    rex_done.markCompleted()
    rex_pending = Task("Evening walk", "18:00", Frequency.DAILY)
    whiskers_pending = Task("Breakfast", "08:00", Frequency.DAILY)
    scheduler.scheduleTask(rex, rex_done)
    scheduler.scheduleTask(rex, rex_pending)
    scheduler.scheduleTask(whiskers, whiskers_pending)

    rex_tasks = scheduler.filter_by_pet(rex)
    pending_rex_tasks = scheduler.filter_by_status(False, rex_tasks)

    assert pending_rex_tasks == [rex_pending]


def test_complete_task_schedules_next_daily_occurrence():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    task = Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    scheduler.scheduleTask(pet, task)

    next_task = scheduler.complete_task(pet, task)

    assert task.completed is True
    assert next_task.completed is False
    assert next_task.description == "Morning walk"
    assert next_task.time == "07:00"
    assert next_task.dueDate == date(2026, 1, 16)
    assert pet.taskList == [task, next_task]


def test_complete_task_schedules_next_weekly_occurrence():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    task = Task("Grooming", "10:00", Frequency.WEEKLY, dueDate=date(2026, 1, 15))
    scheduler.scheduleTask(pet, task)

    next_task = scheduler.complete_task(pet, task)

    assert next_task.dueDate == date(2026, 1, 22)


def test_complete_task_schedules_next_monthly_occurrence_across_month_end():
    owner = Owner("Sam")
    pet = Pet("Whiskers", "cat", 5)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    task = Task("Vet checkup", "16:00", Frequency.MONTHLY, dueDate=date(2026, 1, 31))
    scheduler.scheduleTask(pet, task)

    next_task = scheduler.complete_task(pet, task)

    assert next_task.dueDate == date(2026, 2, 28)


def test_complete_task_monthly_wraps_into_next_year():
    owner = Owner("Sam")
    pet = Pet("Whiskers", "cat", 5)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    task = Task("Vet checkup", "16:00", Frequency.MONTHLY, dueDate=date(2026, 12, 15))
    scheduler.scheduleTask(pet, task)

    next_task = scheduler.complete_task(pet, task)

    assert next_task.dueDate == date(2027, 1, 15)


def test_find_same_pet_conflicts_detects_overlap_for_one_pet():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    walk = Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    meds = Task("Give meds", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    scheduler.scheduleTask(pet, walk)
    scheduler.scheduleTask(pet, meds)

    conflicts = scheduler.find_same_pet_conflicts()

    assert conflicts == [(pet, walk, meds)]
    assert scheduler.find_cross_pet_conflicts() == []


def test_find_cross_pet_conflicts_detects_overlap_across_pets():
    owner = Owner("Sam")
    rex = Pet("Rex", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 5)
    owner.addPet(rex)
    owner.addPet(whiskers)
    scheduler = Scheduler(owner)

    rex_walk = Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    whiskers_breakfast = Task("Breakfast", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    scheduler.scheduleTask(rex, rex_walk)
    scheduler.scheduleTask(whiskers, whiskers_breakfast)

    conflicts = scheduler.find_cross_pet_conflicts()

    assert conflicts == [(rex, rex_walk, whiskers, whiskers_breakfast)]
    assert scheduler.find_same_pet_conflicts() == []


def test_conflicts_ignore_different_times_and_due_dates():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    scheduler.scheduleTask(pet, Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15)))
    scheduler.scheduleTask(pet, Task("Evening walk", "18:00", Frequency.DAILY, dueDate=date(2026, 1, 15)))
    scheduler.scheduleTask(pet, Task("Vet checkup", "07:00", Frequency.MONTHLY, dueDate=date(2026, 1, 16)))

    assert scheduler.find_same_pet_conflicts() == []
    assert scheduler.find_cross_pet_conflicts() == []


def test_conflicts_ignore_completed_tasks():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    walk = Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    meds = Task("Give meds", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    scheduler.scheduleTask(pet, walk)
    scheduler.scheduleTask(pet, meds)
    walk.markCompleted()

    assert scheduler.find_same_pet_conflicts() == []


def test_get_conflict_warnings_reports_both_kinds():
    owner = Owner("Sam")
    rex = Pet("Rex", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 5)
    owner.addPet(rex)
    owner.addPet(whiskers)
    scheduler = Scheduler(owner)

    scheduler.scheduleTask(rex, Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15)))
    scheduler.scheduleTask(rex, Task("Give meds", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15)))
    scheduler.scheduleTask(whiskers, Task("Breakfast", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15)))

    warnings = scheduler.get_conflict_warnings()

    assert len(warnings) == 3  # 1 same-pet pair + 2 cross-pet pairs (rex's 2 tasks x whiskers' 1 task)
    assert any("Rex has" in w for w in warnings)
    assert any("Rex's" in w and "Whiskers" in w for w in warnings)
