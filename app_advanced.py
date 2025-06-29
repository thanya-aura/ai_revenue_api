import streamlit as st
import requests

st.set_page_config(page_title="Advanced Revenue Agent")
st.title("📊 Revenue Advanced Analysis")

uploaded_file = st.file_uploader("Upload Excel file with advanced data", type=["xlsx"])

if uploaded_file:
    with st.spinner("Sending to API..."):
        files = {"file": uploaded_file}
        response = requests.post("http://127.0.0.1:8000/analyze/advanced", files=files)

    if response.status_code == 200:
        result = response.json()
        st.success("✅ Analysis Complete")
        st.write("Message:", result["message"])
        st.write("Projects found:", result["projects"])
    else:
        st.error(f"❌ Error: {response.json()['detail']}")
