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

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time | Sorts by HH:MM |
| Filtering | Scheduler.filter_by_pet & Scheduler.filter_by_status | Shows tasks based on the pet & shows tasks based on done/pending status |
| Conflict handling | Scheduler.find_same_pet_conflicts & Scheduler.find_cross_pet_conflicts | Detects tasks scheduled at the same time for the same pet & detects different tasks scheduled at the same time for different pets |
| Recurring tasks | Scheduler.complete_task | Schedules the next task based on daily, weekly, or monthly frequency |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
