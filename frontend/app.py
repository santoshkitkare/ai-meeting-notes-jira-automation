import streamlit as st
import time
import json
from api import create_job, get_job_status

st.set_page_config(page_title="AI Meeting → Jira", layout="centered")

st.title("🤖 AI Meeting → Jira Automation")
st.write("Paste a YouTube or Zoom meeting link and generate Jira tasks automatically.")

# Input
url = st.text_input("Meeting URL")
source_type = st.selectbox("Source Type", ["youtube", "zoom"])

if st.button("🚀 Process Meeting"):

    if not url:
        st.error("Please enter a meeting URL")
    else:
        with st.spinner("Submitting job..."):
            job = create_job(url, source_type)
            job_id = job["job_id"]

        st.success("Job submitted successfully!")
        st.info(f"Job ID: {job_id}")

        status_box = st.empty()

        while True:
            result = get_job_status(job_id)

            if result["status"] == "COMPLETED":
                st.success("Processing completed!")
                break

            elif result["status"] == "FAILED":
                st.error("Job failed.")
                st.stop()

            status_box.info("Processing... Please wait ⏳")
            time.sleep(5)

        # Show results
        parsed = json.loads(result["result"])

        st.subheader("📝 Summary")
        st.write(parsed.get("summary", ""))

        st.subheader("📌 Action Items")
        for item in parsed.get("action_items", []):
            st.markdown(f"**• {item['title']}**  \nPriority: {item.get('priority', 'N/A')}")

        if "jira_tickets" in parsed:
            st.subheader("🎫 Jira Tickets")
            for ticket in parsed["jira_tickets"]:
                st.markdown(f"🔗 [{ticket['key']}]({ticket['url']})")