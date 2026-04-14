import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from streamlit_lottie import st_lottie
from streamlit_extras.metric_cards import style_metric_cards

# ==========================================
# 1. PAGE SETUP & THEME
# ==========================================
st.set_page_config(
    page_title="TaskFlow // NOIR",
    page_icon="💛",
    layout="wide"
)

# Function to load animations safely
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Reliable Lottie Links
lottie_user = load_lottieurl("https://lottie.host/82547087-73d3-4674-897d-4187034c56e9/D2y9P5wFis.json")
lottie_success = load_lottieurl("https://lottie.host/8075677d-8646-444c-9f6f-215034870f2b/O6yF1XGZ5A.json")

# ==========================================
# 2. CUSTOM CSS (BLACK & YELLOW)
# ==========================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #000000;
            color: #FFFFFF;
        }

        .stApp { background-color: #000000; }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0A0A0A;
            border-right: 2px solid #FFD700;
        }

        /* Yellow Headers */
        h1, h2, h3 {
            color: #FFD700 !important;
            font-weight: 900 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Professional Buttons */
        .stButton>button {
            background-color: #000000;
            color: #FFD700;
            border: 2px solid #FFD700;
            border-radius: 4px;
            font-weight: 700;
            transition: 0.3s;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #FFD700;
            color: #000000;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
        }

        /* Metric Card Customization */
        [data-testid="stMetric"] {
            background-color: #0A0A0A;
            border: 1px solid #333333;
            padding: 15px;
            border-radius: 10px;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; }
        .stTabs [data-baseweb="tab"] {
            background-color: #0A0A0A;
            border: 1px solid #333333;
            color: #FFFFFF;
            padding: 10px 20px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #FFD700 !important;
            color: #000000 !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. DATA PERSISTENCE LOGIC
# ==========================================
if 'tasks_df' not in st.session_state:
    try:
        st.session_state.tasks_df = pd.read_csv('tasks.csv')
    except:
        st.session_state.tasks_df = pd.DataFrame(columns=[
            "ID", "Task Name", "Timeframe", "Deadline", "Priority", "Status"
        ])

def save_tasks():
    st.session_state.tasks_df.to_csv('tasks.csv', index=False)

# ==========================================
# 4. SIDEBAR - COMMAND CENTER
# ==========================================
with st.sidebar:
    # Safety Check for Animation
    if lottie_user:
        st_lottie(lottie_user, height=150, key="nav_anim")
    else:
        st.title("💛")
        
    st.title("NOIR // OPS")
    st.markdown("---")
    
    with st.form("input_form", clear_on_submit=True):
        name = st.text_input("OBJECTIVE", placeholder="Enter task name...")
        time = st.selectbox("TIMEFRAME", ["Daily", "Weekly", "Monthly", "Backlog"])
        prio = st.select_slider("PRIORITY", options=["Low", "Medium", "High", "CRITICAL"])
        date = st.date_input("DEADLINE", datetime.now())
        
        if st.form_submit_button("DEPLOY TASK"):
            if name:
                new_data = pd.DataFrame([{
                    "ID": datetime.now().strftime("%H%M%S"),
                    "Task Name": name,
                    "Timeframe": time,
                    "Deadline": date.strftime("%Y-%m-%d"),
                    "Priority": prio,
                    "Status": "Pending"
                }])
                st.session_state.tasks_df = pd.concat([st.session_state.tasks_df, new_data], ignore_index=True)
                save_tasks()
                st.toast("Task Synced to Database", icon="⚡")
                st.rerun()

# ==========================================
# 5. MAIN INTERFACE
# ==========================================
st.title("SYSTEM // TASKFLOW // DASHBOARD")

# Top Metrics
df = st.session_state.tasks_df
c1, c2, c3 = st.columns(3)
c1.metric("TOTAL OBJECTIVES", len(df))
c2.metric("PENDING", len(df[df["Status"] == "Pending"]))
c3.metric("CRITICAL", len(df[df["Priority"] == "CRITICAL"]))
style_metric_cards(background_color="#0A0A0A", border_color="#FFD700", border_size_px=1)

st.markdown("---")

tab1, tab2 = st.tabs(["🚀 ACTIVE MISSIONS", "⚙️ SYSTEM LOGS"])

with tab1:
    if df.empty:
        st.info("No active tasks. Deploy from the sidebar.")
    else:
        # Task Table with interactivity
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
            key="editor",
            disabled=["ID"]
        )
        if not edited_df.equals(df):
            st.session_state.tasks_df = edited_df
            save_tasks()
            st.rerun()

with tab2:
    st.subheader("Database Management")
    if st.button("PURGE ALL DATA"):
        st.session_state.tasks_df = pd.DataFrame(columns=df.columns)
        save_tasks()
        st.warning("Database cleared.")
        st.rerun()
    
    st.download_button(
        "EXPORT SYSTEM BACKUP",
        data=df.to_csv(index=False),
        file_name="task_backup.csv",
        mime="text/csv"
    )

st.markdown("""
    <div style="position: fixed; bottom: 10px; width: 100%; text-align: center; color: #444;">
        NOIR v1.0 // ENCRYPTED SESSION
    </div>
""", unsafe_allow_html=True)