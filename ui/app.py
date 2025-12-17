import os
import streamlit as st
import requests

ORCH_URL = os.getenv("ORCH_URL", "http://orchestrator-service:8000/agent/standup")

st.set_page_config(page_title="AI Daily Stand-up Assistant", page_icon="🤖", layout="wide")
st.title("🤖 AI Daily Stand-up Assistant")

st.caption(
    "Developer token hint: run "
    "`python scripts/generate_jwt.py --sub developer-1 --role Developer --name \"Developer User\" --key keys/dev-jwt.key --hours 24` "
    "and paste the output JWT below."
)

token = st.text_input("Bearer token", type="password", placeholder="Paste JWT here")
user_id = st.number_input("User ID", min_value=1, value=1)
message = st.text_area("Enter your stand-up update", height=200)

st.markdown("**Optional notification** (requires a valid JWT and a ScrumMaster/Admin role):")
send_notification = st.checkbox("Send summary notification", value=False)
notify_to = st.text_input("Notify recipient (email/WhatsApp)", placeholder="user@example.com or +15555555555")
notify_channel = st.selectbox("Channel", ["email", "whatsapp"])
notify_subject = st.text_input("Notification subject", value="Standup Summary")
if send_notification and not token:
    st.info("Notification uses the MCP notification tool; it requires a valid JWT.")

if st.button("Submit"):
    with st.spinner("Agent analyzing your update..."):
        payload = {"user_id": user_id, "message": message}
        if token:
            payload["token"] = token
        if send_notification and notify_to:
            payload["notify_to"] = notify_to
            payload["notify_channel"] = notify_channel
            if notify_subject:
                payload["notify_subject"] = notify_subject
        try:
            r = requests.post(ORCH_URL, json=payload, timeout=60)
            r.raise_for_status()
            data = r.json()
            st.subheader("Extracted Tasks & Delay Risk")
            st.json(data.get("tasks", []))
            st.subheader("AI Summary for Scrum Master")
            st.write(data.get("summary", ""))
            if data.get("notification") is not None:
                st.subheader("Notification result")
                st.json(data["notification"])
        except requests.RequestException as ex:
            st.error(f"Request failed: {ex}")
            st.text(r.text if 'r' in locals() else "")
        except ValueError as ex:
            st.error(f"Bad JSON response: {ex}")
            st.text(r.text if 'r' in locals() else "")
