import streamlit as st
import requests

st.title("Ask the Server")

service_account = st.text_input("Enter your Service Account")
question = st.text_input("What question do you want to ask?")

if st.button("Ask"):
    if not service_account or not question:
        st.warning("Please provide both a service account and a question.")
    else:
        try:
            backend_url = "https://your-backend-url.com/ask"

            response = requests.post(
                backend_url,
                json={"serviceAccount": service_account, "question": question},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                st.success(f"Server Response: {data.get('answer', 'No answer received')}")
            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"Failed to connect to server: {e}")
