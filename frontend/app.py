import streamlit as st
import time
import json
import requests
from api import create_job, get_job_status, get_all_jobs

st.set_page_config(page_title="AI Meeting → Jira", layout="centered")

# -------------------------
# Session State Init
# -------------------------
if "job_id" not in st.session_state:
    st.session_state.job_id = None

if "job_result" not in st.session_state:
    st.session_state.job_result = None

if "selected_items" not in st.session_state:
    st.session_state.selected_items = {}

if "jira_links" not in st.session_state:
    st.session_state.jira_links = []
# -------------------------
# UI
# -------------------------
st.title("🤖 AI Meeting → Jira Automation")

url = st.text_input("Meeting URL")
source_type = st.selectbox("Source Type", ["youtube", "zoom"])

# -------------------------
# Submit Job
# -------------------------
if st.button("🚀 Process Meeting"):
    if not url:
        st.error("Please enter a meeting URL")
    else:
        job = create_job(url, source_type)
        st.session_state.job_id = job["job_id"]

        with st.spinner("Processing meeting..."):
            while True:
                result = get_job_status(st.session_state.job_id)
                if result["status"] == "COMPLETED":
                    st.session_state.job_result = json.loads(result["result"])
                    break
                time.sleep(3)

# -------------------------
# Render Results
# -------------------------
if st.session_state.job_result:
    parsed = st.session_state.job_result

    st.subheader("📝 Summary")
    st.write(parsed.get("summary", ""))

    st.subheader("📄 Decisions")

    decisions = parsed.get("decisions", [])

    if decisions:
        for idx, decision in enumerate(decisions, start=1):
            st.markdown(f"**{idx}.** {decision}")
    else:
        st.info("No decisions found.")

    st.subheader("📌 Action Items")

    for idx, item in enumerate(parsed.get("action_items", [])):
        key = f"chk_{idx}"

        col1, col2, col3, col4, col5 = st.columns([0.05, 0.2, 0.45, 0.15, 0.15])

        with col1:
            st.session_state.selected_items[key] = st.checkbox(
                label="Select",
                key=key,
                label_visibility="collapsed"
            )
        with col2:
            st.markdown(f"**{item['title']}**")

        with col3:
            st.write(item["description"])

        with col4:
            st.write(item["owner"])

        with col5:
            st.write(item["priority"])

    # -------------------------
    # Jira Creation
    # -------------------------
    selected = [
        item
        for idx, item in enumerate(parsed["action_items"])
        if st.session_state.selected_items.get(f"chk_{idx}")
    ]


    if selected:
        if st.button("🚀 Create Jira Tickets"):
            res = requests.post(
                f"http://localhost:8000/jobs/{st.session_state.job_id}/jira",
                json=selected
            )

            jira_data = res.json().get("jira_tickets", [])
            st.session_state.jira_links = jira_data
            if "jira_links" in st.session_state:
                st.subheader("🎫 Jira Tickets")

                for j in st.session_state["jira_links"]:
                    st.markdown(f"🔗 [{j['key']}]({j['url']})")


    else:
        st.info("Select action items to create Jira tickets.")

st.header("📜 Job History")

jobs = get_all_jobs()

for job in jobs:
    with st.expander(f"🆔 {job['job_id']} | {job['status']}"):

        job_data = get_job_status(job["job_id"])

        st.write("### Summary")
        parsed = json.loads(job_data["result"])
        st.write(parsed.get("summary"))

        st.write("### Action Items")
        for item in parsed.get("action_items", []):
            st.markdown(f"- {item['title']}")

        st.write("### Jira Tickets")
        if job_data.get("jira_tickets"):
            for j in job_data["jira_tickets"]:
                st.markdown(f"🔗 [{j['key']}]({j['url']})")
        else:
            st.info("No Jira tickets created")
