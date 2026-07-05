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

One constraint the scheduler considers is scheduling conflicts. I thought this was important because the purpose of the app is to allow pet owners to organize themselves properly to provide proper care for their pets. Without considering scheduling conflicts, this would defeat the app's purpose.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler makes the tradeoff of not considering task duration. This is because the app is meant to be used by a wide array of pet owners. Some owners may allow tasks to run longer than other owners would. I do not believe it is the app developer's responsibility to tell a user how much time they should spend walking their dog for example. The downside is that users may end up ignoring their schedule and running late for other tasks. In the future, perhaps a notification system can be implemented in the app to help keep pet owners on track, but ultimately it is up to the owner to determine to what extent they want to stick to the schedule they have created.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI in all aspects of the project, including: refactoring, code generation, and design implementation. I had some questions regarding my initial design. Claude was instrumental in helping guide me on some choices I should make in terms of who should own tasks. Class design is not one of my strengths and Claude made some suggestions that were logical and considered that I had not initially.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One case where I did not accept Claude's suggestion as it was, was when it suggested how users should be warned of scheduling conflicts. I ran the app myself and realized that the message that was generated for scheduling conflicts was something that I could easily miss. I suggested to Claude that the message should be a pop-up message that explained the conflict to the user and asked them if they want to proceed anyway. This way, users are steered to acknowledge the warning.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I instructed Claude to test all changes early on. Anytime a new feature was implemented Claude created a test for all methods involved and ran them. I also made sure to test the app myself by running it after every feature. This is because I wanted to see for myself that the app was working as intended.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm fairly confident that the scheduler works correctly. The one edge case I would test next has to do with running concurrent tasks. Some tasks can be done simultaneously by a pet owner, but not necessarily all of them. My implementation is currently able to handle identical tasks for different pets (e.g., taking two dogs for a walk), but it currently doesn't consider a case where a friend walks one dog, while the pet owner takes the other dog to the vet.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with being able to implement the filtering logic. This is because it was not clear to me from the beginning what the best way would be to do it. Claude was super helpful in this regard, and the filtering logic worked as I had envisioned it.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would do more work on the UI. It still seems unpolished. I would expand the schedule itself to allow users to mark tasks as done. Currently, the user has to go back up to the pet section and mark tasks as being complete there.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned how powerful Claude is when it comes to design. My first implementation was a little convoluted in terms of what classes did what. However, this also made me aware of how my own lack of experience can make Claude lead me and my projects to a place I had not intended. This shows how important it is for me to still do my own research to have a deeper understanding of system design.
