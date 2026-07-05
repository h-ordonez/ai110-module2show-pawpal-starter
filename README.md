# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule

Rex (dog):
  07:00 AM - Morning walk
  12:00 PM - Lunchtime feeding
  06:30 PM - Evening walk

Whiskers (cat):
  08:00 AM - Breakfast
  01:30 PM - Litter box cleaning
  04:00 PM - Vet checkup
```

## 🧪 Testing PawPal+

The command I used to run tests was `python -m pytest`. There are 43 tests in all and they cover all methods pawpal_system.py. The methods they cover implement sorting, filtering, automation of recurring tasks, and basic conflict detection.

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
(.venv) PS C:\Users\hordo\Projects\ai110-module2show-pawpal-starter> pytest
====================================================================== test session starts =======================================================================
platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\hordo\Projects\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0, cov-7.1.0
collected 43 items                                                                                                                                                

tests\test_pawpal.py ...........................................                                                                                            [100%]

======================================================================= 43 passed in 0.06s =======================================================================
```

My confidence level in the system's reliability is 4/5 stars. This is because the tests offer great coverage as I found out when running `pytest --cov`. However, the reason why I don't give it the full 5/5 stars is because I have yet to see it deployed and used by a lot of people. If it were to actually be deployed to a large population, I would not be surprised if some more bugs were uncovered as is so often the case.

## 📐 Smarter Scheduling

PawPal+ doesn't just store a flat task list — the `Scheduler` implements a few small algorithms to keep that list organized and useful:

### ✨ Features

- **Task sorting** — `Scheduler.sort_by_time` turns each task's `"HH:MM"` string into an `(hour, minute)` tuple and sorts on that, so tasks land in true chronological order (no lexicographic surprises like `"9:00"` sorting after `"10:00"`). Standard O(n log n) sort under the hood.
- **Filtering** — `Scheduler.filter_by_pet` and `Scheduler.filter_by_status` do a single O(n) pass over the task list. Pet filtering checks *identity*, not value — a task is only "Rex's" if it's literally the same object in Rex's list, so two tasks that happen to look identical (same description/time) but belong to different pets never get mixed up.
- **Conflict detection** — `find_same_pet_conflicts`, `find_cross_pet_conflicts`, and `get_conflict_warnings` avoid the naive O(n²) approach of comparing every task to every other task. `_pending_slots` first buckets all pending tasks by `(due date, time)` in a single O(n) pass; only tasks that land in the *same* slot are ever compared to each other. From there:
  - **Same-pet conflict**: one pet has two pending tasks in the same slot (e.g. Rex can't be walked and bathed at 7:00 AM).
  - **Cross-pet conflict**: two different pets have pending tasks in the same slot — unless it's the exact same activity (e.g. both pets going on one walk together isn't a conflict, it's one event).
- **Recurring tasks** — `Scheduler.complete_task` marks a task done, then `Task.next_due_date` computes when it recurs next based on `Frequency`: daily adds 1 day, weekly adds 7 days, monthly rolls to the same day next month (clamped to the last valid day via `calendar.monthrange`, so e.g. Jan 31 → Feb 28). A new `Task` is created for that date and automatically added back to the pet's schedule, so routine care never has to be re-entered by hand.

### Quick reference

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time | Sorts by HH:MM |
| Filtering | Scheduler.filter_by_pet & Scheduler.filter_by_status | Shows tasks based on the pet & shows tasks based on done/pending status |
| Conflict handling | Scheduler.find_same_pet_conflicts & Scheduler.find_cross_pet_conflicts | Detects tasks scheduled at the same time for the same pet & detects different tasks scheduled at the same time for different pets |
| Recurring tasks | Scheduler.complete_task | Schedules the next task based on daily, weekly, or monthly frequency |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Enter your name in the Owner field
2. Add one or more pets
3. Add zero or more tasks for each pet
4. Observe the auto-generated schedule for the tasks you have entered
5. Mark tasks as done for each pet
6. Optionally, you can remove pets/tasks

`main.py` CLI output:
```
(.venv) PS C:\Users\hordo\Projects\ai110-module2show-pawpal-starter> python main.py
Today's Schedule (before completing anything)

Rex (dog):
  2026-01-15 06:30 PM - Evening walk (pending)
  2026-01-15 07:00 AM - Morning walk (pending)
  2026-01-15 12:00 PM - Lunchtime feeding (pending)
  2026-01-15 06:30 PM - Give meds (pending)

Fido (dog):
  2026-01-15 06:30 PM - Evening walk (pending)

Whiskers (cat):
  2026-01-31 04:00 PM - Vet checkup (pending)
  2026-01-15 08:00 AM - Breakfast (pending)
  2026-01-15 01:30 PM - Litter box cleaning (pending)
  2026-01-15 06:30 PM - Grooming (pending)

Completing Morning walk, Breakfast, Litter box cleaning, and Vet checkup...

Today's Schedule (after completing - note the auto-scheduled next occurrences)

Rex (dog):
  2026-01-15 06:30 PM - Evening walk (pending)
  2026-01-15 07:00 AM - Morning walk (done)
  2026-01-15 12:00 PM - Lunchtime feeding (pending)
  2026-01-15 06:30 PM - Give meds (pending)
  2026-01-16 07:00 AM - Morning walk (pending)

Fido (dog):
  2026-01-15 06:30 PM - Evening walk (pending)

Whiskers (cat):
  2026-01-31 04:00 PM - Vet checkup (done)
  2026-01-15 08:00 AM - Breakfast (done)
  2026-01-15 01:30 PM - Litter box cleaning (done)
  2026-01-15 06:30 PM - Grooming (pending)
  2026-01-16 08:00 AM - Breakfast (pending)
  2026-01-16 01:30 PM - Litter box cleaning (pending)
  2026-02-28 04:00 PM - Vet checkup (pending)

filter_by_pet(rex):
  2026-01-15 06:30 PM - Evening walk (pending)
  2026-01-15 07:00 AM - Morning walk (done)
  2026-01-15 12:00 PM - Lunchtime feeding (pending)
  2026-01-15 06:30 PM - Give meds (pending)
  2026-01-16 07:00 AM - Morning walk (pending)

filter_by_pet(whiskers):
  2026-01-31 04:00 PM - Vet checkup (done)
  2026-01-15 08:00 AM - Breakfast (done)
  2026-01-15 01:30 PM - Litter box cleaning (done)
  2026-01-15 06:30 PM - Grooming (pending)
  2026-01-16 08:00 AM - Breakfast (pending)
  2026-01-16 01:30 PM - Litter box cleaning (pending)
  2026-02-28 04:00 PM - Vet checkup (pending)

filter_by_status(completed=True):
  2026-01-15 07:00 AM - Morning walk (done)
  2026-01-31 04:00 PM - Vet checkup (done)
  2026-01-15 08:00 AM - Breakfast (done)
  2026-01-15 01:30 PM - Litter box cleaning (done)

filter_by_status(completed=False):
  2026-01-15 06:30 PM - Evening walk (pending)
  2026-01-15 12:00 PM - Lunchtime feeding (pending)
  2026-01-15 06:30 PM - Give meds (pending)
  2026-01-16 07:00 AM - Morning walk (pending)
  2026-01-15 06:30 PM - Evening walk (pending)
  2026-01-15 06:30 PM - Grooming (pending)
  2026-01-16 08:00 AM - Breakfast (pending)
  2026-01-16 01:30 PM - Litter box cleaning (pending)
  2026-02-28 04:00 PM - Vet checkup (pending)

find_same_pet_conflicts():
  Rex: 'Evening walk' vs 'Give meds' at 06:30 PM on 2026-01-15

find_cross_pet_conflicts():
  Rex's 'Evening walk' vs Whiskers's 'Grooming' at 06:30 PM on 2026-01-15
  Rex's 'Give meds' vs Fido's 'Evening walk' at 06:30 PM on 2026-01-15
  Rex's 'Give meds' vs Whiskers's 'Grooming' at 06:30 PM on 2026-01-15
  Fido's 'Evening walk' vs Whiskers's 'Grooming' at 06:30 PM on 2026-01-15

get_conflict_warnings():
  [!] Conflict: Rex has 'Evening walk' and 'Give meds' both scheduled at 18:30 on 2026-01-15.
  [!] Conflict: Rex's 'Evening walk' and Whiskers's 'Grooming' are both scheduled at 18:30 on 2026-01-15.
  [!] Conflict: Rex's 'Give meds' and Fido's 'Evening walk' are both scheduled at 18:30 on 2026-01-15.
  [!] Conflict: Rex's 'Give meds' and Whiskers's 'Grooming' are both scheduled at 18:30 on 2026-01-15.
  [!] Conflict: Fido's 'Evening walk' and Whiskers's 'Grooming' are both scheduled at 18:30 on 2026-01-15.
```
**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
