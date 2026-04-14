import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from streamlit_lottie import st_lottie

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="TaskFlow OS", page_icon="⚡", layout="wide")

# 2. APPLE-STYLE GLASSMORPHISM CSS
st.markdown("""
    <style>
        /* Import clean Typography */
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;600&family=Inter:wght@400;700&display=swap');

        /* Global Styling */
        .stApp {
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
            color: #ffffff;
        }

        /* Frosted Glass Sidebar */
        [data-testid="stSidebar"] {
            background-color: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 215, 0, 0.2);
        }

        /* Glass Cards for Metrics */
        div[data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 215, 0, 0.1);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        /* Apple-style Yellow Button */
        .stButton>button {
            background: #FFD700;
            color: #000000;
            border: none;
            border-radius: 12px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3);
            background: #ffdb1a;
        }

        /* Clean Tabs */
        .stTabs [data-baseweb="tab-list"] { gap: 24px; }
        .stTabs [data-baseweb="tab"] {
            font-family: 'SF Pro Display', sans-serif;
            font-size: 18px;
            color: #888;
            border: none;
        }
        .stTabs [aria-selected="true"] {
            color: #FFD700 !important;
            border-bottom: 2px solid #FFD700 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. DATA & LOGIC
if 'tasks_df' not in st.session_state:
    st.session_state.tasks_df = pd.DataFrame(columns=["Task", "Category", "Priority", "Status"])

# 4. SIDEBAR (THE INPUT)
with st.sidebar:
    st.markdown("<h1 style='font-size: 24px;'>TaskFlow <span style='color:#FFD700;'>OS</span></h1>", unsafe_allow_html=True)
    with st.form("add_task", clear_on_submit=True):
        name = st.text_input("Objective")
        cat = st.selectbox("Timeline", ["Daily", "Weekly", "Monthly"])
        prio = st.select_slider("Priority", options=["Low", "Medium", "High"])
        if st.form_submit_button("Deploy Task"):
            new_row = pd.DataFrame([{"Task": name, "Category": cat, "Priority": prio, "Status": "Active"}])
            st.session_state.tasks_df = pd.concat([st.session_state.tasks_df, new_row], ignore_index=True)
            st.rerun()

# 5. MAIN CONTENT
st.markdown("<h1 style='text-align: center; font-weight: 800;'>Control Center</h1>", unsafe_allow_html=True)

# Metric Row
c1, c2, c3 = st.columns(3)
c1.metric("Active Missions", len(st.session_state.tasks_df))
c2.metric("Efficiency", "94%", delta="2%")
c3.metric("Uptime", "100%")

st.markdown("<br>", unsafe_allow_html=True)

# Organized Tabs
t1, t2 = st.tabs([" Roadmap", " Archive"])

with t1:
    if st.session_state.tasks_df.empty:
        st.write("---")
        st.caption("No active objectives. Initiate a task from the sidebar.")
    else:
        for i, row in st.session_state.tasks_df.iterrows():
            # Minimalist Task Card
            with st.container():
                col_a, col_b = st.columns([4,1])
                col_a.markdown(f"**{row['Task']}** \n`{row['Category']}` | Priority: {row['Priority']}")
                if col_b.button("Done", key=f"btn_{i}"):
                    st.session_state.tasks_df = st.session_state.tasks_df.drop(i)
                    st.balloons()
                    st.rerun()
                st.markdown("---")