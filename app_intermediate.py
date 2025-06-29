import streamlit as st
import requests

st.set_page_config(page_title="Intermediate Revenue Agent")
st.title("📊 Revenue Intermediate Analysis")

uploaded_file = st.file_uploader("Upload Excel file with multiple sheets", type=["xlsx"])

if uploaded_file:
    with st.spinner("Sending to API..."):
        files = {"file": uploaded_file}
        response = requests.post("http://127.0.0.1:8000/analyze/intermediate", files=files)

    if response.status_code == 200:
        result = response.json()
        st.success("✅ Analysis Complete")
        for project, data in result.items():
            st.subheader(project)
            st.metric("Planned", data["total_planned"])
            st.metric("Actual", data["total_actual"])
            st.metric("Variance", data["total_variance"])
    else:
        st.error(f"❌ Error: {response.json()['detail']}")
