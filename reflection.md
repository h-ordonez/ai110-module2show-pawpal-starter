# PawPal+ Project Reflection

## 1. System Design

There are three core actions a user should be able to perform. First, the user should be able to add a pet. Second, a user should be able to schedule tasks. Finally, a user should be able to get notification reminders of the tasks that need to be completed.

**a. Initial design**

- Briefly describe your initial UML design.

    My initial UML design was based on owners, pets, tasks, and schedulers.
    

- What classes did you include, and what responsibilities did you assign to each?

    My UML design contains four classes. They are the Owner, Pet, Task, and Scheduler. Thwe owner has one or many pets. The owner has zero or many tasks. The scheduler manages an owner. Finally, the scheduler assigns tasks.

    The owner was responsible for having pets and scheduling tasks. The pet class was nothing more than a data container with no methods. The task class was responsible for checking whether a task had been completed or not. I had initially left the scheduler class blank because I was somewhat lost on what its responsibilites should be after creating the other classes. Fortunately, Claude helped in this regard.

**b. Design changes**

- Did your design change during implementation?

    Yes.

- If yes, describe at least one change and why you made it.

    A change I made was to add a Pet reference to Task. This was because Claude explained that the getTasksByPet method would not be able to be implemented otherwise. The motiviation behind implementing this change was due to the fact that an Owner might want to know what tasks they have to complete for a particular pet, and there would have been no way of knowing this with the previous design.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
