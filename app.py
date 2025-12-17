import streamlit as st
import pandas as pd

st.set_page_config(page_title="Production Goal Calculator", layout="centered")
st.title("Production Line Goal Calculator")

# ---- CONSTANTS ----
RATE_PER_PERSON = 1.74
TIME_BLOCKS = [
    "05:30–06:30","06:30–07:30","07:30–08:30","08:30–09:30",
    "09:30–10:30","10:30–11:30","11:30–12:30","12:30–13:30",
    "13:30–14:30","14:30–15:00"
]

# ---- ATTENDANCE ----
st.header("Attendance")

if "people" not in st.session_state:
    st.session_state.people = []  # List of all added people

if "selected" not in st.session_state:
    st.session_state.selected = []  # People currently present

# Add new person
new_person = st.text_input("Add a person")
if st.button("Add Person"):
    if new_person and new_person not in st.session_state.people:
        st.session_state.people.append(new_person)
        st.success(f"{new_person} added!")
    elif new_person in st.session_state.people:
        st.warning(f"{new_person} is already in the list.")

# Display attendance checkboxes
if st.session_state.people:
    st.write("Select present people:")
    for person in st.session_state.people:
        if st.checkbox(person, key=person, value=person in st.session_state.selected):
            if person not in st.session_state.selected:
                st.session_state.selected.append(person)
        else:
            if person in st.session_state.selected:
                st.session_state.selected.remove(person)

headcount = len(st.session_state.selected)
st.success(f"Total People Present: {headcount}")

# ---- PRODUCTION INPUT ----
st.header("Production Units per Time Block")
units = {}
for time in TIME_BLOCKS:
    units[time] = st.number_input(f"{time}", min_value=0.0, step=0.5, key=time)

# ---- SUBMIT ----
if st.button("Submit"):
    if headcount == 0:
        st.error("Please select at least one person present.")
    else:
        goal = round(RATE_PER_PERSON * headcount, 1)

        data = []
        for time in TIME_BLOCKS:
            data.append({
                "Time": time,
                "Units": units[time],
                "Goal": goal
            })

        df = pd.DataFrame(data)

        st.header("Results")
        st.dataframe(df, use_container_width=True)

        st.metric("Hourly Goal", goal)
        st.metric("Total Units", df["Units"].sum())
        st.metric("Total Goal (All Hours)", round(goal * len(TIME_BLOCKS),1))
