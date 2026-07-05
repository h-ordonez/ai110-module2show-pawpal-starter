from datetime import time

import streamlit as st
from pawpal_system import Frequency
from pawpal_system import Task
from pawpal_system import Pet
from pawpal_system import Owner
from pawpal_system import Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

st.session_state.owner.name = owner_name

st.markdown("### Pets")
st.caption("Add pets via Owner.addPet(). Remove them via Owner.removePet().")

pcol1, pcol2, pcol3 = st.columns([2, 2, 1])
with pcol1:
    pet_name = st.text_input("Pet name", value="Mochi")
with pcol2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with pcol3:
    st.write("")
    if st.button("Add pet"):
        st.session_state.owner.addPet(Pet(name=pet_name, species=species, age=0))

if st.session_state.owner.petList:
    for p in list(st.session_state.owner.petList):
        rcol1, rcol2 = st.columns([4, 1])
        with rcol1:
            st.write(f"🐾 {p.name} ({p.species})")
        with rcol2:
            if st.button("Remove", key=f"remove_pet_{id(p)}"):
                st.session_state.owner.removePet(p)
                st.rerun()
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add tasks via Scheduler.scheduleTask(), remove via Scheduler.removeTask(), "
            "mark done via Task.markCompleted().")

if not st.session_state.owner.petList:
    st.info("Add a pet above before adding tasks.")
else:
    pet_names = [p.name for p in st.session_state.owner.petList]
    selected_pet_name = st.selectbox("Pet", pet_names)
    selected_pet = next(p for p in st.session_state.owner.petList if p.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_time = st.time_input("Time", value=time(8, 0))
    with col3:
        task_frequency = st.selectbox("Frequency", [f.value for f in Frequency], index=0)

    if st.button("Add task"):
        new_task = Task(
            description=task_title,
            time=task_time.strftime("%H:%M"),
            frequency=Frequency(task_frequency),
        )
        st.session_state.scheduler.scheduleTask(selected_pet, new_task)

    current_tasks = st.session_state.scheduler.getTasksByPet(selected_pet)
    if current_tasks:
        st.write("Current tasks:")
        for t in list(current_tasks):
            tcol1, tcol2, tcol3, tcol4, tcol5 = st.columns([3, 1.5, 1.5, 1.5, 1])
            with tcol1:
                st.write(t.description)
            with tcol2:
                st.write(t.time)
            with tcol3:
                st.write(t.frequency.value)
            with tcol4:
                done = st.checkbox("Done", value=t.completed, key=f"done_{id(t)}")
                if done and not t.completed:
                    t.markCompleted()
            with tcol5:
                if st.button("Remove", key=f"remove_task_{id(t)}"):
                    st.session_state.scheduler.removeTask(selected_pet, t)
                    st.rerun()
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Uses Scheduler.getAllTasks() to pull every task across the owner's pets, ordered by time.")

if st.button("Generate schedule"):
    pet_tasks = [
        (p, t)
        for p in st.session_state.owner.petList
        for t in st.session_state.scheduler.getTasksByPet(p)
    ]
    if not pet_tasks:
        st.info("No tasks to schedule yet. Add some tasks above.")
    else:
        pet_by_task_id = {id(t): p for p, t in pet_tasks}
        ordered = st.session_state.scheduler.sort_by_time([t for _, t in pet_tasks])
        st.write("Today's plan:")
        st.table(
            [
                {
                    "time": t.time,
                    "pet": pet_by_task_id[id(t)].name,
                    "task": t.description,
                    "frequency": t.frequency.value,
                }
                for t in ordered
            ]
        )
