
import streamlit as st
import requests

st.title("Airspace Copilot Demo")
identifier = st.text_input("Enter Flight Callsign", "THY4KZ")

if st.button("Track Flight"):
    resp = requests.get("http://127.0.0.1:8000/tools/flights.get", params={"identifier": identifier})
    if resp.status_code == 200:
        st.json(resp.json())
    else:
        st.error("Flight not found")
