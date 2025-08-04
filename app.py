import streamlit as st
from datetime import datetime, timedelta, date
import json
import os
import random

# Set page config at the very top (global for entire app)
st.set_page_config(page_title="Govardhani Space", layout="centered")

# Dummy login credentials for 2 users
USERS = {
    "govardhani": "Jennie.2005",
    "verma": "exe"  # Example password for your brother
}

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# def safe_rerun():
#     # Safe rerun by toggling a session_state variable to force refresh
#     if "rerun_trigger" not in st.session_state:
#         st.session_state.rerun_trigger = False
#     st.session_state.rerun_trigger = not st.session_state.rerun_trigger

if not st.session_state.logged_in:
    st.title("🔐 Login to Govardhani Space")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success(f"Login successful! Welcome {username}.")
            st.rerun()
        else:
            st.error("Invalid credentials. Try again.")

else:
    user = st.session_state.user
    user_data_dir = f"data/{user}"
    os.makedirs(user_data_dir, exist_ok=True)

    TASKS_FILE = os.path.join(user_data_dir, "tasks.json")
    TODO_FILE = os.path.join(user_data_dir, "todo.json")
    HABITS_FILE = os.path.join(user_data_dir, "habits.json")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "To-Do List", "Habits", "Portfolio", "My calendar"])

    # Header & greeting
    st.title(f"Welcome to Govardhani Space 🚀")
    st.subheader(f"Hello {user.capitalize()}! Today is {datetime.now().strftime('%A, %d %B %Y')}")

    quotes = [
        "Push yourself, because no one else is going to do it for you.",
        "Success doesn’t just find you. You have to go out and get it.",
        "Dream it. Believe it. Build it.",
        "Small steps every day lead to big results."
    ]
    st.info(random.choice(quotes))

    # Load tasks_by_date globally for calendar/home
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            tasks_by_date = json.load(f)
    else:
        tasks_by_date = {}

    if page == "Home":
        st.write("📌 This is your personal dashboard. Add your daily picture, track goals, and stay inspired!")

        # Load todo tasks for progress bar
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r") as f:
                tasks = json.load(f)
        else:
            tasks = []

        if tasks:
            total = len(tasks)
            completed = sum(task["done"] for task in tasks)
            percent = int((completed / total) * 100)

            st.write(f"✅ You’ve completed {completed} out of {total} tasks ({percent}%)")
            st.progress(percent)

            st.bar_chart({"Completed": completed, "Pending": total - completed})
        else:
            st.info("No tasks yet. Add some in the To-Do List section!")

        st.subheader("📊 Weekly Summary")
        today = datetime.today()
        week_dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        weekly_task_count = sum(len(tasks_by_date.get(d, [])) for d in week_dates)
        st.write(f"You added **{weekly_task_count} tasks** this week! Keep going 💪")

    elif page == "My calendar":
        st.title("📅 My Calendar Task Tracker")

        selected_date = st.date_input("Choose a date to view or add tasks", value=date.today())
        date_str = selected_date.strftime("%Y-%m-%d")

        st.subheader(f"📝 Add Task for {date_str}")
        task_input = st.text_input("Enter your task")

        if st.button("Add Task"):
            if task_input.strip():
                tasks_by_date.setdefault(date_str, []).append({"task": task_input, "done": False})
                with open(TASKS_FILE, "w") as f:
                    json.dump(tasks_by_date, f)
                st.success("Task added!")
                st.rerun()
            else:
                st.warning("Please enter a valid task.")

        st.subheader(f"📌 Tasks on {date_str}")
        if date_str in tasks_by_date and tasks_by_date[date_str]:
            changed = False
            updated_tasks = []
            for i, task_obj in enumerate(tasks_by_date[date_str]):
                col1, col2, col3 = st.columns([0.05, 0.75, 0.2])
                with col1:
                    done = st.checkbox("", value=task_obj["done"], key=f"{date_str}_done_{i}")
                with col2:
                    st.markdown(f"- {task_obj['task']}")
                with col3:
                    delete = st.button("🗑️ Delete", key=f"{date_str}_del_{i}")

                if delete:
                    continue  # Skip adding this task to updated list (i.e., delete it)
                else:
                    task_obj["done"] = done
                    updated_tasks.append(task_obj)

            # Update tasks and save
            tasks_by_date[date_str] = updated_tasks
            with open(TASKS_FILE, "w") as f:
                json.dump(tasks_by_date, f)

            if changed:
                with open(TASKS_FILE, "w") as f:
                    json.dump(tasks_by_date, f)
        else:
            st.info("No tasks found for this date.")

    elif page == "To-Do List":
        st.title("📝 Your To-Do List")
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r") as f:
                tasks = json.load(f)
        else:
            tasks = []

        new_task = st.text_input("Add a new task")
        if st.button("Add Task") and new_task:
            tasks.append({"task": new_task, "done": False})
            with open(TODO_FILE, "w") as f:
                json.dump(tasks, f)
            st.rerun()

        updated_tasks = []
        for i, task in enumerate(tasks):
            col1, col2, col3 = st.columns([0.05, 0.75, 0.2])
            with col1:
                checked = st.checkbox("", value=task["done"], key=f"todo_done_{i}")
            with col2:
                st.markdown(f"- {task['task']}")
            with col3:
                delete = st.button("🗑️ Delete", key=f"todo_delete_{i}")

            if not delete:
                updated_tasks.append({"task": task["task"], "done": checked})

        # Save updated task list
        with open(TODO_FILE, "w") as f:
            json.dump(updated_tasks, f)

    elif page == "Habits":
        st.title("📊 Habit Tracker")
        if os.path.exists(HABITS_FILE):
            with open(HABITS_FILE, "r") as f:
                habit_data = json.load(f)
        else:
            habit_data = {}

        new_habit = st.text_input("Add a new habit")
        if st.button("Add Habit") and new_habit:
            if new_habit not in habit_data:
                habit_data[new_habit] = []
                with open(HABITS_FILE, "w") as f:
                    json.dump(habit_data, f)
                st.rerun()

        st.subheader("🌿 Track Today's Habits")
        today_str = datetime.now().strftime("%Y-%m-%d")
        changed = False
        for habit in habit_data:
            checked = st.checkbox(habit, key=f"habit_{habit}", value=today_str in habit_data[habit])
            if checked and today_str not in habit_data[habit]:
                habit_data[habit].append(today_str)
                changed = True
            elif not checked and today_str in habit_data[habit]:
                habit_data[habit].remove(today_str)
                changed = True
        if changed:
            with open(HABITS_FILE, "w") as f:
                json.dump(habit_data, f)

        st.subheader("📊 This Month's Progress")
        current_month = datetime.now().strftime("%Y-%m")
        for habit, dates in habit_data.items():
            count = sum(1 for d in dates if d.startswith(current_month))
            st.write(f"✅ **{habit}**: {count} times this month")

    elif page == "Portfolio":
        st.title("💼 Govardhani's Portfolio")

        st.markdown("Hi, I'm **Govardhani**! I’m passionate about tech, open-source, and building projects that solve real-world problems.")

        st.markdown("### 🎓 Department")
        st.write("B.Tech in Internet of Things (IoT)")

        st.markdown("### 🛠️ Tech Skills")
        st.write("- **Current:** Python, C, HTML, Golang")
        st.write("- **Learning:** SQL, DSA")
        st.write("- **Also familiar with:** IoT systems, computer fundamentals")

        st.markdown("### 🧰 Tech Stack")
        tech_stack = [
            "🧠 Python, C, Go",
            "🌐 RESTful APIs (Postman, Thunder Client)",
            "📦 Git & GitHub",
            "🖥️ Streamlit for UI & deployment",
            "🔌 Arduino & sensor integration",
            "🗣️ ai4bharat/IndicTrans for multilingual NLP",
            "🧪 SQL (learning phase)",
            "🐧 Linux commands & VS Code"
        ]
        for tech in tech_stack:
            st.markdown(f"- {tech}")

        st.markdown("### 🌐 Connect with Me")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("[🔗 GitHub](https://github.com/GGovardhani)")
        with col2:
            st.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/govardhani-gokaraju-gg)")

        st.markdown("### 🧪 Projects I've Worked On")
        st.write("- 🎮 **Mini Python Games**: Rock-Paper-Scissors, Number Guessing Game")
        st.write("- ✅ **Task Manager App**: Built in Python to manage daily tasks")
        st.write("- 🌐 **Personal Portfolio**: Showcasing my skills and projects")
        st.write("- 🤖 **Chatbots & AI**: Integrating NLP models")
        st.write("- 🔌 **IoT Projects**: Sensor data collection and visualization")

# You can add any additional helper functions or utilities below if needed
