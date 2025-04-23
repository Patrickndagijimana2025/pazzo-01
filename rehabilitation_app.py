import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Rehabilitation Tracker", page_icon="🏋️", layout="wide")

# Add custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stMetric {
        font-size: 18px;
        font-weight: bold;
    }
    footer {
        text-align: center;
        font-size: 14px;
        margin-top: 50px;
        color: #888;
    }
    header {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add a header
st.markdown(
    """
    <header>
        🏋️ Welcome to the Rehabilitation Management App!
    </header>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for storing exercise data
if 'exercise_data' not in st.session_state:
    st.session_state.exercise_data = pd.DataFrame(columns=['Date', 'Exercise', 'Reps', 'Duration', 'Notes', 'Feeling', 'Pain Level'])

# Initialize session state for goals
if 'goals' not in st.session_state:
    st.session_state.goals = pd.DataFrame(columns=['Goal', 'Target Date', 'Progress', 'Notes'])

# Initialize session state for appointments
if 'appointments' not in st.session_state:
    st.session_state.appointments = pd.DataFrame(columns=['Date', 'Time', 'Description'])

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["🏠 Home", "📝 Log Exercise", "📊 View Progress", "🎯 Set Goals", "📅 Schedule Appointment"]
)

# Home Page
if page == "🏠 Home":
    st.header("Welcome to the Rehabilitation Management App! 🎉")
    st.write("This app helps you manage your rehabilitation exercises, set goals, and track your progress.")

    #  motivational quote
    st.markdown(
        """
        > *"The difference between the impossible and the possible lies in a person's determination."*  
        **- Tommy Lasorda**
        > *"Ntawuzaguhesha agaciro nutiha agaciro "*  
        **- Paul Kagame**
        > *"Run if you cant walk if you cant crawl no matter what just keep moving"*  
        **- martin luther king**

        """
    )

    # Display a summary of logged data
    st.subheader("Your Progress Summary 📊")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Exercises Logged", len(st.session_state.exercise_data))
    with col2:
        st.metric("Goals Set", len(st.session_state.goals))
    with col3:
        st.metric("Appointments Scheduled", len(st.session_state.appointments))

    
    st.image("pic.jpg", width=500, caption="Stay Motivated!")  # Adjust the width as needed

    # Add quick navigation buttons
    st.subheader("Quick Navigation 🚀")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Log Exercise"):
            page = "📝 Log Exercise"
    with col2:
        if st.button("View Progress"):
            page = "📊 View Progress"
    with col3:
        if st.button("Set Goals"):
            page = "🎯 Set Goals"

# Log Exercise Page
elif page == "📝 Log Exercise":
    st.header("Log Your Exercise 📝")
    with st.form("log_exercise_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", datetime.date.today())
            exercise = st.text_input("Exercise Name")
            reps = st.number_input("Repetitions", min_value=0, step=1)
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=0.0, step=0.1)
            notes = st.text_area("Notes")
        feeling = st.selectbox("How did you feel during the exercise?", ["Select", "Good 😊", "Okay 😐", "Bad 😞"])
        pain_level = st.slider("Pain Level (0-10)", 0, 10, 0)
        if st.form_submit_button("Log Exercise"):
            new_entry = pd.DataFrame({
                'Date': [date],
                'Exercise': [exercise],
                'Reps': [reps],
                'Duration': [duration],
                'Notes': [notes],
                'Feeling': [feeling],
                'Pain Level': [pain_level]
            })
            st.session_state.exercise_data = pd.concat([st.session_state.exercise_data, new_entry], ignore_index=True)
            st.success("Exercise logged successfully! ✅")

# View Progress Page
elif page == "📊 View Progress":
    st.header("Your Exercise Progress 📊")
    if st.session_state.exercise_data.empty:
        st.info("No exercise data logged yet. Start logging your exercises to see progress!")
    else:
        st.write(st.session_state.exercise_data)
        st.subheader("Exercise Duration Over Time 📈")
        fig = px.bar(
            st.session_state.exercise_data,
            x="Date",
            y="Duration",
            title="Exercise Duration Over Time",
            labels={"Duration": "Duration (minutes)", "Date": "Date"},
            color="Duration",
        )
        st.plotly_chart(fig)

# Set Goals Page
elif page == "🎯 Set Goals":
    st.header("Set Your Rehabilitation Goals 🎯")
    with st.form("set_goals_form"):
        col1, col2 = st.columns(2)
        with col1:
            goal = st.text_input("Goal Description")
            target_date = st.date_input("Target Date", datetime.date.today())
        with col2:
            progress = st.number_input("Progress (%)", min_value=0, max_value=100, step=1)
            notes = st.text_area("Notes")
        if st.form_submit_button("Add Goal"):
            new_goal = pd.DataFrame({
                'Goal': [goal],
                'Target Date': [target_date],
                'Progress': [progress],
                'Notes': [notes]
            })
            st.session_state.goals = pd.concat([st.session_state.goals, new_goal], ignore_index=True)
            st.success("Goal added successfully! 🎉")
    if not st.session_state.goals.empty:
        st.subheader("Your Goals 📋")
        for index, row in st.session_state.goals.iterrows():
            st.write(f"**{row['Goal']}** (Target Date: {row['Target Date']})")
            st.progress(row['Progress'] / 100)
    else:
        st.info("No goals set yet. Start setting your goals to track progress!")

# Schedule Appointment Page
elif page == "📅 Schedule Appointment":
    st.header("Schedule an Appointment 📅")
    with st.form("schedule_appointment_form"):
        appointment_date = st.date_input("Appointment Date", datetime.date.today())
        appointment_time = st.time_input("Appointment Time", datetime.time(9, 0))
        description = st.text_input("Description of Appointment")
        if st.form_submit_button("Schedule Appointment"):
            new_appointment = pd.DataFrame({
                'Date': [appointment_date],
                'Time': [appointment_time],
                'Description': [description]
            })
            st.session_state.appointments = pd.concat([st.session_state.appointments, new_appointment], ignore_index=True)
            st.success("Appointment scheduled successfully! ✅")
    if not st.session_state.appointments.empty:
        st.subheader("Your Appointments 📅")
        st.write(st.session_state.appointments)
    else:
        st.info("No appointments scheduled yet.")

# Add a footer
st.markdown(
    """
    <footer>
        © 2025 Rehabilitation Management App. All rights reserved Ndagijimana Patrick.
    </footer>
    """,
    unsafe_allow_html=True,
)