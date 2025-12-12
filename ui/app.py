import os
import streamlit as st
import requests

ORCH_URL = os.getenv("ORCH_URL", "http://orchestrator-service:8000/agent/standup")

st.set_page_config(page_title="AI Daily Stand-up Assistant", page_icon="🤖", layout="wide")
st.title("🤖 AI Daily Stand-up Assistant")

token = st.text_input("Bearer token", type="password")
user_id = st.number_input("User ID", min_value=1, value=1)
message = st.text_area("Enter your stand-up update", height=200)

if st.button("Submit"):
    with st.spinner("Agent analyzing your update..."):
        payload = {"user_id": user_id, "message": message}
        if token:
            payload["token"] = token
        try:
            r = requests.post(ORCH_URL, json=payload, timeout=60)
            r.raise_for_status()
            data = r.json()
            st.subheader("Extracted Tasks & Delay Risk")
            st.json(data.get("tasks", []))
            st.subheader("AI Summary for Scrum Master")
            st.write(data.get("summary", ""))
        except requests.RequestException as ex:
            st.error(f"Request failed: {ex}")
            st.text(r.text if 'r' in locals() else "")
        except ValueError as ex:
            st.error(f"Bad JSON response: {ex}")
            st.text(r.text if 'r' in locals() else "")
