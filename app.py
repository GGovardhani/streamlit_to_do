import streamlit as st
from datetime import datetime,timedelta
from datetime import date
import json
import os
import random

# Dummy login credentials
USERNAME = "govardhani"
PASSWORD = "Jennie.2005"  # Replace with a secure method later

# Login logic
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login to Govardhani Space")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials. Try again.")
else:
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "To-Do List", "Habits", "Portfolio","My calender"])

    # Header
    st.title("Welcome to Govardhani Space 🚀")
    st.subheader(f"Hello Govardhani! Today is {datetime.now().strftime('%A, %d %B %Y')}")

    # Motivational Quote
    quotes = [
        "Push yourself, because no one else is going to do it for you.",
        "Success doesn’t just find you. You have to go out and get it.",
        "Dream it. Believe it. Build it.",
        "Small steps every day lead to big results."
    ]
    st.info(random.choice(quotes))
    # ---------- Load tasks_by_date for use in both Home and Calendar ----------
    TASKS_FILE = "tasks.json"
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            tasks_by_date = json.load(f)
    else:
        tasks_by_date = {}

    # Page Routing
    if page == "Home":
        st.write("📌 This is your personal dashboard. Add your daily picture, track goals, and stay inspired!")
        if "tasks" in st.session_state and st.session_state.tasks:
            total = len(st.session_state.tasks)
            completed = sum(task["done"] for task in st.session_state.tasks)
            percent = int((completed / total) * 100)

            st.write(f"✅ You’ve completed {completed} out of {total} tasks ({percent}%)")
            st.progress(percent)

            st.bar_chart({"Completed": completed, "Pending": total - completed})
        else:
            st.info("No tasks yet. Add some in the To-Do List section!")
            
        st.subheader("📊 Weekly Summary")
        # Get last 7 days
        today = datetime.today()
        week_dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        # Count tasks from last 7 days
        weekly_task_count = sum(len(tasks_by_date.get(date, [])) for date in week_dates)
        st.write(f"You added **{weekly_task_count} tasks** this week! Keep going 💪")

        st.subheader("📷 Daily Picture Upload")

        uploaded_file = st.file_uploader("Upload your daily photo", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            st.image(uploaded_file, caption="Your uploaded photo", use_column_width=True)
    elif page == "My calender":
        st.set_page_config(page_title="📅 Calendar Task Tracker", layout="centered")

        st.title("📅 My Calendar Task Tracker")

        # ---------- Load tasks from file ----------
        TASKS_FILE = "tasks.json"

        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                tasks_by_date = json.load(f)
        else:
            tasks_by_date = {}

        # ---------- Select a date ----------
        selected_date = st.date_input("Choose a date to view or add tasks", value=date.today())
        date_str = selected_date.strftime("%Y-%m-%d")

        # ---------- Add a new task ----------
        st.subheader(f"📝 Add Task for {date_str}")
        task_input = st.text_input("Enter your task")

        if st.button("Add Task"):
            if task_input.strip():
                tasks_by_date.setdefault(date_str, []).append({"task": task_input, "done": False})
                with open(TASKS_FILE, "w") as f:
                    json.dump(tasks_by_date, f)
                st.success("Task added!")
            else:
                st.warning("Please enter a valid task.")

        # ---------- Display tasks for selected date ----------
        st.subheader(f"📌 Tasks on {date_str}")
        if date_str in tasks_by_date and tasks_by_date[date_str]:
            for i, task_obj in enumerate(tasks_by_date[date_str]):
                col1, col2 = st.columns([0.05, 0.95])
                with col1:
                    done = st.checkbox("", value=task_obj["done"], key=f"{date_str}_{i}")
                with col2:
                    st.markdown(f"- {task_obj['task']}")
                # Update task status
                tasks_by_date[date_str][i]["done"] = done
            # Save updated status
            with open(TASKS_FILE, "w") as f:
                json.dump(tasks_by_date, f)
        else:
            st.info("No tasks found for this date.")
            

    
    elif page == "To-Do List":
        st.write("📝 Your tasks for today:")
        TODO_FILE = "todo.json"

        # Load tasks from file
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r") as f:
                st.session_state.tasks = json.load(f)
        else:
            st.session_state.tasks = []

        # Add new task
        new_task = st.text_input("Add a new task")
        if st.button("Add Task") and new_task:
            st.session_state.tasks.append({"task": new_task, "done": False})
            with open(TODO_FILE, "w") as f:
                json.dump(st.session_state.tasks, f)

        # Display tasks with checkboxes
        for i, task in enumerate(st.session_state.tasks):
            checked = st.checkbox(task["task"], value=task["done"], key=i)
            st.session_state.tasks[i]["done"] = checked

        # Save updated task status
        with open(TODO_FILE, "w") as f:
            json.dump(st.session_state.tasks, f)
                # Add to-do list logic here
    elif page == "Habits":
        st.write("📊 Track your habits:")
        DATA_FILE = "habits.json"

        # Load habit history
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                habit_data = json.load(f)
        else:
            habit_data = {}

        # Add new habit
        new_habit = st.text_input("Add a new habit")
        if st.button("Add Habit") and new_habit:
            if new_habit not in habit_data:
                habit_data[new_habit] = []
                with open(DATA_FILE, "w") as f:
                    json.dump(habit_data, f)

        # Display habits
        st.subheader("🌿 Track Today's Habits")
        today = datetime.now().strftime("%Y-%m-%d")

        for habit in habit_data:
            if st.checkbox(habit):
                if today not in habit_data[habit]:
                    habit_data[habit].append(today)
                    with open(DATA_FILE, "w") as f:
                        json.dump(habit_data, f)

        # Monthly count
        st.subheader("📊 This Month's Progress")
        current_month = datetime.now().strftime("%Y-%m")

        for habit, dates in habit_data.items():
            count = sum(1 for d in dates if d.startswith(current_month))
            st.write(f"✅ **{habit}**: {count} times this month")
                # Add habit tracker logic here
    elif page == "Portfolio":
        st.write("💼 Your projects and skills:")
        st.title("💼 Govardhani's Portfolio")

        st.markdown("Hi, I'm **Govardhani**! I’m passionate about tech, open-source, and building projects that solve real-world problems.")

        st.markdown("### 🎓 Department")
        st.write("B.Tech in Internet of Things (IoT)")

        st.markdown("### 🛠️ Tech Skills")
        st.write("- **Current:** Python, C, HTML,Golang")
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
            st.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/govardhani-gokaraju-gg)")  # Replace with your actual LinkedIn URL

        st.markdown("### 🧪 Projects I've Worked On")
        st.write("- 🎮 **Mini Python Games**: Rock-Paper-Scissors, Number Guessing Game")
        st.write("- ✅ **Task Manager App**: Built in Python to manage daily tasks")
        st.write("- 🌐 **Personal Portfolio**: Showcasing my work and skills")

        st.markdown("### 🚀 Featured Projects")
        projects = [
            {
                "title": "Smart Drain Shield System",
                "description": "An IoT-based system to detect waterlogging and send geo-tagged alerts.",
                "tech": "Arduino, Sensors, Python, Streamlit",
                "link": "https://github.com/govardhani/smart-drain-shield"
            },
            {
                "title": "Multilingual AI Chatbot",
                "description": "Supports Indic languages using ai4bharat/IndicTrans integration.",
                "tech": "Python, Hugging Face, Streamlit",
                "link": "https://github.com/govardhani/indic-chatbot"
            },
            {
                "title": "My Life Dashboard",
                "description": "A personal productivity dashboard with habits, tasks, and daily uploads.",
                "tech": "Python, Streamlit, JSON",
                "link": "https://github.com/govardhani/my-life-dashboard"
            }
        ]

        for project in projects:
            st.markdown(f"#### {project['title']}")
            st.write(project["description"])
            st.write(f"**Tech Stack:** {project['tech']}")
            st.markdown(f"[🔗 GitHub Link]({project['link']})")
            st.markdown("---")

        st.markdown("### 📜 Certifications & Workshops")
        st.write("- CS50: Introduction to Computer Science – NPTEL")
        st.write("- Introduction to IoT – SkillDzire")
        st.write("- Participated in Drone Technology Workshop")

        st.markdown("### 🌟 Aspirations")
        st.write("I aspire to become a software developer who builds ethical and inclusive technology for everyone.")