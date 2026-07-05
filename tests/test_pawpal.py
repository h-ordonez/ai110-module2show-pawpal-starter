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


def test_scheduling_identical_task_twice_does_not_duplicate():
    # scheduleTask guards with `if task not in pet.taskList`, and Task's dataclass
    # equality is value-based, so re-adding a value-identical Task is a no-op.
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    scheduler.scheduleTask(pet, Task("Morning walk", "07:00", Frequency.DAILY))
    scheduler.scheduleTask(pet, Task("Morning walk", "07:00", Frequency.DAILY))

    assert len(pet.taskList) == 1


def test_remove_task_removes_it_from_pets_task_list():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    task = Task("Morning walk", "07:00", Frequency.DAILY)
    scheduler.scheduleTask(pet, task)

    scheduler.removeTask(pet, task)

    assert pet.taskList == []


def test_remove_task_not_in_list_is_a_noop():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    task = Task("Morning walk", "07:00", Frequency.DAILY)
    scheduler.scheduleTask(pet, task)

    scheduler.removeTask(pet, Task("Evening walk", "18:00", Frequency.DAILY))

    assert pet.taskList == [task]


def test_remove_pet_removes_it_from_owners_pet_list():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)

    owner.removePet(pet)

    assert owner.petList == []


def test_get_tasks_by_pet_returns_only_that_pets_tasks():
    owner = Owner("Sam")
    rex = Pet("Rex", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 2)
    owner.addPet(rex)
    owner.addPet(whiskers)
    scheduler = Scheduler(owner)

    rex_task = Task("Morning walk", "07:00", Frequency.DAILY)
    scheduler.scheduleTask(rex, rex_task)
    scheduler.scheduleTask(whiskers, Task("Breakfast", "08:00", Frequency.DAILY))

    assert scheduler.getTasksByPet(rex) == [rex_task]


def test_get_all_tasks_aggregates_across_every_pet():
    owner = Owner("Sam")
    rex = Pet("Rex", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 2)
    owner.addPet(rex)
    owner.addPet(whiskers)
    scheduler = Scheduler(owner)

    scheduler.scheduleTask(rex, Task("Morning walk", "07:00", Frequency.DAILY))
    scheduler.scheduleTask(whiskers, Task("Breakfast", "08:00", Frequency.DAILY))

    assert len(scheduler.getAllTasks()) == 2


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


def test_sort_by_time_with_no_tasks_returns_empty_list():
    owner = Owner("Sam")
    scheduler = Scheduler(owner)

    assert scheduler.sort_by_time() == []


def test_sort_by_time_is_stable_for_tasks_sharing_a_time():
    # Python's sort is stable, so equal-time tasks should keep their scheduling order
    # rather than being reordered arbitrarily - important since two tasks at the same
    # time are exactly the case find_same_pet_conflicts is meant to flag separately.
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    first = Task("Walk", "07:00", Frequency.DAILY)
    second = Task("Meds", "07:00", Frequency.DAILY)
    scheduler.scheduleTask(pet, first)
    scheduler.scheduleTask(pet, second)

    ordered = scheduler.sort_by_time()

    assert [t.description for t in ordered] == ["Walk", "Meds"]


def test_sort_by_time_composes_with_filter_by_pet():
    owner = Owner("Sam")
    rex = Pet("Rex", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 2)
    owner.addPet(rex)
    owner.addPet(whiskers)
    scheduler = Scheduler(owner)

    scheduler.scheduleTask(rex, Task("Evening walk", "18:00", Frequency.DAILY))
    scheduler.scheduleTask(rex, Task("Morning walk", "07:00", Frequency.DAILY))
    scheduler.scheduleTask(whiskers, Task("Breakfast", "06:00", Frequency.DAILY))

    ordered = scheduler.sort_by_time(scheduler.filter_by_pet(rex))

    assert [t.description for t in ordered] == ["Morning walk", "Evening walk"]


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


def test_filter_by_pet_distinguishes_value_equal_tasks_from_other_pets():
    # filter_by_pet compares by identity, not Task's value-based dataclass equality,
    # so when two different pets have a task with identical field values -
    # description, time, frequency, completed, dueDate - filtering by one pet does
    # NOT leak in the other pet's value-equal task.
    #
    # This is not a contrived case: it's exactly the "two pets sharing the same
    # activity" scenario the app explicitly supports elsewhere (see
    # test_cross_pet_conflicts_exempt_identical_shared_tasks).
    owner = Owner("Sam")
    rex = Pet("Rex", "dog", 3)
    fido = Pet("Fido", "dog", 2)
    owner.addPet(rex)
    owner.addPet(fido)
    scheduler = Scheduler(owner)

    rex_walk = Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    fido_walk = Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    scheduler.scheduleTask(rex, rex_walk)
    scheduler.scheduleTask(fido, fido_walk)

    assert scheduler.filter_by_pet(rex) == [rex_walk]
    assert scheduler.filter_by_pet(fido) == [fido_walk]


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


def test_next_due_date_daily_advances_one_day():
    task = Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))

    assert task.next_due_date() == date(2026, 1, 16)


def test_next_due_date_daily_wraps_into_next_year():
    task = Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 12, 31))

    assert task.next_due_date() == date(2027, 1, 1)


def test_next_due_date_weekly_advances_seven_days():
    task = Task("Grooming", "10:00", Frequency.WEEKLY, dueDate=date(2026, 1, 15))

    assert task.next_due_date() == date(2026, 1, 22)


def test_next_due_date_weekly_wraps_into_next_year():
    task = Task("Grooming", "10:00", Frequency.WEEKLY, dueDate=date(2026, 12, 28))

    assert task.next_due_date() == date(2027, 1, 4)


def test_next_due_date_monthly_clamps_at_shorter_month_end():
    task = Task("Vet checkup", "16:00", Frequency.MONTHLY, dueDate=date(2026, 1, 31))

    assert task.next_due_date() == date(2026, 2, 28)


def test_next_due_date_monthly_clamps_to_leap_day():
    # 2028 is a leap year, so Feb has 29 days - the clamp should land on Feb 29,
    # not skip past it the way a naive Feb 28 clamp would.
    task = Task("Vet checkup", "16:00", Frequency.MONTHLY, dueDate=date(2028, 1, 31))

    assert task.next_due_date() == date(2028, 2, 29)


def test_next_due_date_monthly_wraps_into_next_year():
    task = Task("Vet checkup", "16:00", Frequency.MONTHLY, dueDate=date(2026, 12, 15))

    assert task.next_due_date() == date(2027, 1, 15)


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


def test_complete_task_does_not_mutate_original_tasks_description_or_frequency():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    task = Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    scheduler.scheduleTask(pet, task)

    next_task = scheduler.complete_task(pet, task)

    assert task.description == "Morning walk"
    assert task.frequency == Frequency.DAILY
    assert next_task.frequency == Frequency.DAILY
    assert next_task is not task


def test_complete_task_chains_across_repeated_completions():
    # Completing the freshly-scheduled next occurrence should keep advancing by the
    # same cadence, and every occurrence should accumulate on the pet's task list.
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    task = Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    scheduler.scheduleTask(pet, task)

    second = scheduler.complete_task(pet, task)
    third = scheduler.complete_task(pet, second)

    assert second.dueDate == date(2026, 1, 16)
    assert third.dueDate == date(2026, 1, 17)
    assert third.completed is False
    assert pet.taskList == [task, second, third]


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


def test_find_same_pet_conflicts_with_three_overlapping_tasks_yields_every_pair():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    a = Task("Walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    b = Task("Meds", "07:00", Frequency.WEEKLY, dueDate=date(2026, 1, 15))
    c = Task("Brushing", "07:00", Frequency.MONTHLY, dueDate=date(2026, 1, 15))
    scheduler.scheduleTask(pet, a)
    scheduler.scheduleTask(pet, b)
    scheduler.scheduleTask(pet, c)

    conflicts = scheduler.find_same_pet_conflicts()

    assert len(conflicts) == 3
    assert {(t1.description, t2.description) for _, t1, t2 in conflicts} == {
        ("Walk", "Meds"),
        ("Walk", "Brushing"),
        ("Meds", "Brushing"),
    }


def test_find_same_pet_conflicts_flags_identical_descriptions_on_same_pet():
    # Unlike the cross-pet exemption, two tasks on the SAME pet at the same slot are
    # always a conflict even if they share a description - a pet can't run "Walk" on
    # both a daily and a weekly cadence at once, so this must not be silently exempted.
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    daily_walk = Task("Walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    weekly_walk = Task("Walk", "07:00", Frequency.WEEKLY, dueDate=date(2026, 1, 15))
    scheduler.scheduleTask(pet, daily_walk)
    scheduler.scheduleTask(pet, weekly_walk)

    assert scheduler.find_same_pet_conflicts() == [(pet, daily_walk, weekly_walk)]


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


def test_conflicts_ignore_completed_tasks_across_pets():
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
    rex_walk.markCompleted()

    assert scheduler.find_cross_pet_conflicts() == []


def test_find_conflicts_with_no_tasks_returns_empty_lists():
    owner = Owner("Sam")
    pet = Pet("Rex", "dog", 3)
    owner.addPet(pet)
    scheduler = Scheduler(owner)

    assert scheduler.find_same_pet_conflicts() == []
    assert scheduler.find_cross_pet_conflicts() == []
    assert scheduler.get_conflict_warnings() == []


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


def test_cross_pet_conflicts_exempt_identical_shared_tasks():
    owner = Owner("Sam")
    rex = Pet("Rex", "dog", 3)
    fido = Pet("Fido", "dog", 2)
    owner.addPet(rex)
    owner.addPet(fido)
    scheduler = Scheduler(owner)

    rex_walk = Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    fido_walk = Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    scheduler.scheduleTask(rex, rex_walk)
    scheduler.scheduleTask(fido, fido_walk)

    assert scheduler.find_cross_pet_conflicts() == []
    assert scheduler.get_conflict_warnings() == []


def test_cross_pet_conflicts_still_flag_different_tasks_at_same_time():
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

    assert scheduler.find_cross_pet_conflicts() == [(rex, rex_walk, whiskers, whiskers_breakfast)]


def test_find_cross_pet_conflicts_with_three_pets_in_same_slot_yields_every_pair():
    owner = Owner("Sam")
    rex = Pet("Rex", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 5)
    tweety = Pet("Tweety", "bird", 1)
    owner.addPet(rex)
    owner.addPet(whiskers)
    owner.addPet(tweety)
    scheduler = Scheduler(owner)

    rex_walk = Task("Morning walk", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    whiskers_breakfast = Task("Breakfast", "07:00", Frequency.DAILY, dueDate=date(2026, 1, 15))
    tweety_cage_clean = Task("Clean cage", "07:00", Frequency.WEEKLY, dueDate=date(2026, 1, 15))
    scheduler.scheduleTask(rex, rex_walk)
    scheduler.scheduleTask(whiskers, whiskers_breakfast)
    scheduler.scheduleTask(tweety, tweety_cage_clean)

    conflicts = scheduler.find_cross_pet_conflicts()

    assert len(conflicts) == 3
    pet_pairs = {(p1.name, p2.name) for p1, _, p2, _ in conflicts}
    assert pet_pairs == {("Rex", "Whiskers"), ("Rex", "Tweety"), ("Whiskers", "Tweety")}
