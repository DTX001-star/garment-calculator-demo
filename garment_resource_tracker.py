import streamlit as st
import pandas as pd
from datetime import date

st.title("🧥 Quản lý Tài Nguyên May Mặc theo Ngày")

# Define shirt types and their resource needs
shirt_resources = {
    "Áo thun": {"fabric": 1.2, "thread": 25, "buttons": 0, "labor_hr": 0.3},
    "Áo sơ mi": {"fabric": 2.0, "thread": 40, "buttons": 6, "labor_hr": 0.5},
    "Áo khoác": {"fabric": 3.0, "thread": 60, "buttons": 8, "labor_hr": 1.0},
}

# Select shirt type
shirt_type = st.selectbox("Chọn loại áo:", list(shirt_resources.keys()))

# Display predefined resources for selected shirt type
st.subheader(f"Tài nguyên mặc định cho {shirt_type}:")
resources = shirt_resources[shirt_type]

st.write(f"- Vải: {resources['fabric']} mét/cái")
st.write(f"- Chỉ: {resources['thread']} mét/cái")
st.write(f"- Nút: {resources['buttons']} cái/cái áo")
st.write(f"- Giờ công: {resources['labor_hr']} giờ/cái")

# Enter production quantity
quantity = st.number_input("Số lượng sản xuất dự kiến:", min_value=1, value=100, step=1)

# Arrival dates for resources
st.subheader("Ngày tài nguyên dự kiến về kho công ty:")

fabric_date = st.date_input("Ngày vải về:", date.today())
thread_date = st.date_input("Ngày chỉ về:", date.today())
buttons_date = st.date_input("Ngày nút về:", date.today())
labor_date = st.date_input("Ngày bắt đầu sản xuất:", date.today())

# Calculations
total_fabric = resources["fabric"] * quantity
total_thread = resources["thread"] * quantity
total_buttons = resources["buttons"] * quantity
total_labor_hours = resources["labor_hr"] * quantity

# Summarize Results
st.subheader("📅 Tổng hợp tài nguyên và thời gian:")

data = {
    "Tài nguyên": ["Vải (mét)", "Chỉ (mét)", "Nút (cái)", "Giờ công (giờ)"],
    "Tổng số lượng": [total_fabric, total_thread, total_buttons, total_labor_hours],
    "Ngày dự kiến về kho": [fabric_date, thread_date, buttons_date, labor_date]
}

summary_df = pd.DataFrame(data)

st.table(summary_df)
