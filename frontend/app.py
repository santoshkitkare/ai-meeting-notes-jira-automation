import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh
import json

# --------------------------------
# Config
# --------------------------------
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Meeting → Jira", layout="centered")

# --------------------------------
# Session State
# --------------------------------
if "job_id" not in st.session_state:
    st.session_state.job_id = None

if "job_result" not in st.session_state:
    st.session_state.job_result = None

if "jira_links" not in st.session_state:
    st.session_state.jira_links = []

# --------------------------------
# UI
# --------------------------------
st.title("🤖 AI Meeting → Jira Automation")

url = st.text_input("Meeting URL")
source_type = st.selectbox("Source Type", ["youtube", "zoom"])

# --------------------------------
# Submit Job
# --------------------------------
if st.button("🚀 Process Meeting"):
    if not url:
        st.error("Please enter a meeting URL")
    else:
        res = requests.post(
            f"{BACKEND_URL}/jobs",
            json={"source_url": url, "type": source_type}
        )

        data = res.json()
        st.session_state.job_id = data["job_id"]
        st.session_state.job_result = None
        st.session_state.jira_links = []

        st.success("Job submitted successfully!")

# --------------------------------
# Poll Job Status
# --------------------------------
if st.session_state.job_id and not st.session_state.job_result:

    st_autorefresh(interval=3000, key="job_poll")

    res = requests.get(
        f"{BACKEND_URL}/jobs/{st.session_state.job_id}"
    )

    data = res.json()
    status = data.get("status")

    if status in ["PENDING", "PROCESSING"]:
        st.info("⏳ Processing meeting...")
        st.progress(50)

    elif status == "COMPLETED":
        st.success("✅ Processing completed!")
        result_raw = data["result"]

        if isinstance(result_raw, str):
            result = json.loads(result_raw)
        else:
            result = result_raw
        st.session_state.job_result = result
        st.rerun()

    elif status == "FAILED":
        st.error("❌ Job failed")

# --------------------------------
# Show Result
# --------------------------------
if st.session_state.job_result:

    result = st.session_state.job_result

    st.subheader("📝 Summary")
    st.write(result.get("summary", ""))

    st.subheader("📄 Decisions")
    for i, d in enumerate(result.get("decisions", []), start=1):
        st.markdown(f"**{i}.** {d}")

    # ----------------------------
    # Action Items
    # ----------------------------
    st.subheader("📌 Action Items")

    selected_items = []

    for idx, item in enumerate(result.get("action_items", [])):
        col1, col2, col3 = st.columns([0.1, 0.6, 0.3])

        with col1:
            checked = st.checkbox(
                "Select",
                key=f"action_{idx}",
                label_visibility="collapsed"
)

        with col2:
            st.write(item["title"])

        with col3:
            st.write(item.get("priority", "Medium"))

        if checked:
            selected_items.append(item)

    # ----------------------------
    # Create Jira Tickets
    # ----------------------------
    if selected_items:
        if st.button("🚀 Create Jira Tickets"):
            res = requests.post(
                f"{BACKEND_URL}/jobs/{st.session_state.job_id}/jira",
                json=selected_items
            )

            st.session_state.jira_links = res.json().get("jira_tickets", [])

    # ----------------------------
    # Show Jira Links
    # ----------------------------
    if st.session_state.jira_links:
        st.subheader("🎫 Jira Tickets Created")

        for j in st.session_state.jira_links:
            st.markdown(f"🔗 [{j['key']}]({j['url']}): {j['title']}")

# --------------------------------
# Job History
# --------------------------------
st.divider()
st.subheader("📜 Job History")

history = requests.get(f"{BACKEND_URL}/jobs").json()
# print("Job history:", history)

for job in history:
    # print("Job entry:", job)
    with st.expander(f"🆔 {job['job_id']} | {job['status']}"):

        if not job.get("result"):
            st.info("No result yet")
            continue

        raw_result = job.get("result")
        raw_jira = job.get("jira_tickets")
        print("Raw jira:", raw_jira)

        # Parse result
        if isinstance(raw_result, str):
            result = json.loads(raw_result)
        else:
            result = raw_result

        # Parse jira tickets
        if raw_jira:
            if isinstance(raw_jira, str):
                jira_tickets = json.loads(raw_jira)
            else:
                jira_tickets = raw_jira
        else:
            jira_tickets = []

        st.subheader("📝 Summary")
        st.write(result.get("summary", ""))

        st.subheader("📄 Decisions")
        for i, d in enumerate(result.get("decisions", []), start=1):
            st.markdown(f"**{i}.** {d}")

        st.subheader("📌 Action Items")
        for item in result.get("action_items", []):
            st.markdown(f"- {item['title']} ({item.get('priority', 'Medium')})")

        if jira_tickets:
            st.subheader("🎫 Jira Tickets")
            for j in jira_tickets:
                st.markdown(f"🔗 [{j['key']}]({j['url']}): {j['title']}")