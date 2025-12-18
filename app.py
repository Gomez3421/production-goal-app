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
def get_goal_for_time(time, base_goal):

    if time in ["11:30–12:30", "14:30–15:00"]:
        return round(base_goal * 0.55, 1)  # ~20 if base is ~36–40
    return base_goal

# ---- SUBMIT ----
# ---- SUBMIT ----
if st.button("Submit"):

    if headcount == 0:
        st.error("Please select at least one person present.")
    else:
        goal = round(RATE_PER_PERSON * headcount, 1)

        rows = []
        total_units = 0

        for time in TIME_BLOCKS:
            u = units[time]
            total_units += u
            rows.append((time, u, goal))

        st.header("Results")

        st.markdown(
            """
            <style>
            .card {
                background-color: #1f2a2e;
                border-radius: 10px;
                padding: 15px;
                width: 100%;
                color: white;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                font-size: 15px;
            }
            th {
                background-color: #2c3b40;
                padding: 8px;
                text-align: center;
            }
            td {
                padding: 8px;
                text-align: center;
                border-bottom: 1px solid #3a4a50;
            }
            .red {
                color: #ff4b4b;
                font-weight: bold;
            }
            .green {
                color: #2ecc71;
                font-weight: bold;
            }
            .total {
                font-weight: bold;
                background-color: #2c3b40;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        table_html = (
            '<div class="card">'
            '<h4 style="text-align:center;">3900-1 - 3900 Series</h4>'
            '<table>'
            '<tr>'
            '<th>Range</th>'
            '<th>U</th>'
            '<th>G</th>'
            '</tr>'
        )

        for time, u, g in rows:
            color = "green" if u >= g else "red"
            table_html += (
                f'<tr>'
                f'<td>{time}</td>'
                f'<td class="{color}">{u}</td>'
                f'<td>{g}</td>'
                f'</tr>'
            )

        table_html += (
            f'<tr class="total">'
            f'<td>TOTAL</td>'
            f'<td>{round(total_units, 1)}</td>'
            f'<td></td>'
            f'</tr>'
            '</table>'
            '</div>'
        )

        st.markdown(table_html, unsafe_allow_html=True)

        st.metric("Hourly Goal", goal)
        st




