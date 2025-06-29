import streamlit as st
import requests

st.set_page_config(page_title="Standard Revenue Agent")
st.title("📊 Revenue Standard Analysis")

uploaded_file = st.file_uploader("Upload Excel file for Standard Agent", type=["xlsx"])

if uploaded_file:
    with st.spinner("Sending to API..."):
        files = {"file": uploaded_file}
        response = requests.post("http://127.0.0.1:8000/analyze/standard", files=files)

    if response.status_code == 200:
        result = response.json()
        st.success("✅ Analysis Complete")
        st.metric("Total Planned", result["total_planned"])
        st.metric("Total Actual", result["total_actual"])
        st.metric("Total Variance", result["total_variance"])
        st.dataframe(result["rows"])
    else:
        st.error(f"❌ Error: {response.json()['detail']}")
